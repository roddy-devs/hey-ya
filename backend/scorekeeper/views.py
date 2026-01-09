from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Max, Min, Count
from .models import Session, Hole
from .serializers import SessionSerializer, SessionListSerializer, HoleSerializer


class SessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing play sessions.
    Supports CRUD operations and custom actions for session management.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own sessions
        return Session.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return SessionListSerializer
        return SessionSerializer

    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """End an active session"""
        session = self.get_object()
        
        if session.end_time is not None:
            return Response(
                {'error': 'Session is already ended'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session.end_time = timezone.now()
        session.save()
        
        serializer = self.get_serializer(session)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def advance_hole(self, request, pk=None):
        """
        Complete the current hole and advance to the next one.
        If hole 10 is completed, increment loops and reset to hole 1.
        """
        session = self.get_object()
        
        if session.end_time is not None:
            return Response(
                {'error': 'Cannot advance hole in ended session'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the current hole (the last one created)
        current_hole = session.holes.order_by('-start_time').first()
        
        if current_hole and current_hole.end_time is None:
            # Complete the current hole
            current_hole.end_time = timezone.now()
            current_hole.calculate_score()
            current_hole.save()
            
            # Update session totals
            session.total_score += current_hole.final_score
            
            # If hole 10 is completed, increment loops
            if current_hole.hole_number == 10:
                session.total_loops += 1
                next_hole_number = 1
                next_loop_index = current_hole.loop_index + 1
            else:
                next_hole_number = current_hole.hole_number + 1
                next_loop_index = current_hole.loop_index
            
            session.save()
        else:
            # First hole or no active hole
            next_hole_number = 1
            next_loop_index = 0
        
        # Create the next hole
        next_hole = Hole.objects.create(
            session=session,
            loop_index=next_loop_index,
            hole_number=next_hole_number
        )
        
        return Response({
            'current_hole': HoleSerializer(next_hole).data,
            'session': SessionSerializer(session).data
        })

    @action(detail=True, methods=['post'])
    def record_ball_drop(self, request, pk=None):
        """Record a ball drop for the current hole"""
        session = self.get_object()
        
        if session.end_time is not None:
            return Response(
                {'error': 'Cannot record ball drop in ended session'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the current hole
        current_hole = session.holes.order_by('-start_time').first()
        
        if not current_hole or current_hole.end_time is not None:
            return Response(
                {'error': 'No active hole'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        current_hole.ball_drops += 1
        current_hole.save()
        
        session.total_ball_drops += 1
        session.save()
        
        return Response({
            'current_hole': HoleSerializer(current_hole).data,
            'session': SessionSerializer(session).data
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get aggregate statistics for the user"""
        user_sessions = self.get_queryset().filter(end_time__isnull=False)
        
        if not user_sessions.exists():
            return Response({
                'message': 'No completed sessions found',
                'stats': {}
            })
        
        stats = {
            'total_sessions': user_sessions.count(),
            'best_score': user_sessions.aggregate(Max('total_score'))['total_score__max'],
            'worst_score': user_sessions.aggregate(Min('total_score'))['total_score__min'],
            'average_score': user_sessions.aggregate(Avg('total_score'))['total_score__avg'],
            'average_loops': user_sessions.aggregate(Avg('total_loops'))['total_loops__avg'],
            'total_loops': user_sessions.aggregate(total=Count('total_loops'))['total'],
        }
        
        # Per-hole statistics
        holes = Hole.objects.filter(session__user=request.user, end_time__isnull=False)
        hole_stats = []
        
        for hole_num in range(1, 11):
            hole_data = holes.filter(hole_number=hole_num)
            if hole_data.exists():
                first_hole = hole_data.order_by('end_time').first()
                hole_stats.append({
                    'hole_number': hole_num,
                    'average_completion_time': hole_data.aggregate(
                        avg_time=Avg('completion_time')
                    )['avg_time'],
                    'fastest_completion': first_hole.completion_time if first_hole else None,
                })
        
        stats['hole_stats'] = hole_stats
        
        return Response(stats)


class HoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing hole data.
    Holes are managed through Session actions.
    """
    serializer_class = HoleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see holes from their own sessions
        return Hole.objects.filter(session__user=self.request.user)

