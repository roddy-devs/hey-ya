from django.contrib import admin
from .models import Session, Hole


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'start_time', 'end_time', 'total_score', 'total_loops', 'total_ball_drops']
    list_filter = ['user', 'start_time', 'end_time']
    search_fields = ['user__username']
    readonly_fields = ['start_time', 'created_at']


@admin.register(Hole)
class HoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'loop_index', 'hole_number', 'start_time', 'end_time', 'final_score', 'ball_drops']
    list_filter = ['hole_number', 'loop_index']
    search_fields = ['session__user__username']
    readonly_fields = ['start_time']

