from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Session, Hole


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class HoleSerializer(serializers.ModelSerializer):
    completion_time = serializers.ReadOnlyField()

    class Meta:
        model = Hole
        fields = [
            'id', 'session', 'loop_index', 'hole_number',
            'start_time', 'end_time', 'completion_time',
            'base_score', 'decay_score', 'final_score', 'ball_drops'
        ]
        read_only_fields = ['start_time', 'base_score', 'decay_score', 'final_score']


class SessionSerializer(serializers.ModelSerializer):
    duration = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    holes = HoleSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = [
            'id', 'user', 'start_time', 'end_time', 'duration',
            'total_score', 'total_ball_drops', 'total_loops',
            'created_at', 'is_active', 'holes'
        ]
        read_only_fields = ['start_time', 'created_at', 'user']


class SessionListSerializer(serializers.ModelSerializer):
    """Lighter serializer for listing sessions without hole details"""
    duration = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Session
        fields = [
            'id', 'user', 'start_time', 'end_time', 'duration',
            'total_score', 'total_ball_drops', 'total_loops',
            'created_at', 'is_active'
        ]
