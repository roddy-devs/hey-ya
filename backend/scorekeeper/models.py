from django.db import models
from django.contrib.auth.models import User


class Session(models.Model):
    """
    Represents one continuous play session for a user.
    A session may include multiple loops.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_score = models.IntegerField(default=0)
    total_ball_drops = models.IntegerField(default=0)
    total_loops = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Session {self.id} - {self.user.username} - {self.start_time}"

    @property
    def duration(self):
        """Calculate session duration if end_time is set"""
        if self.end_time:
            return self.end_time - self.start_time
        return None

    @property
    def is_active(self):
        """Check if session is currently active"""
        return self.end_time is None


class Hole(models.Model):
    """
    Represents a single hole attempt within a session.
    Each hole tracks timing, scoring, and ball drops.
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='holes')
    loop_index = models.IntegerField(default=0)
    hole_number = models.IntegerField()  # 1-10
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    base_score = models.IntegerField(default=0)
    decay_score = models.IntegerField(default=0)
    final_score = models.IntegerField(default=0)
    ball_drops = models.IntegerField(default=0)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"Hole {self.hole_number} - Loop {self.loop_index} - Session {self.session_id}"

    @property
    def completion_time(self):
        """Calculate hole completion time if end_time is set"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def calculate_score(self):
        """
        Calculate final score based on completion time and base score.
        Score decays based on time taken to complete the hole.
        """
        if not self.end_time:
            return 0

        completion_seconds = self.completion_time
        
        # Base scores for holes 1-10 (configurable)
        BASE_SCORES = {
            1: 100, 2: 200, 3: 300, 4: 400, 5: 500,
            6: 600, 7: 700, 8: 800, 9: 900, 10: 1000
        }
        
        self.base_score = BASE_SCORES.get(self.hole_number, 100)
        
        # Decay logic: 1 point lost per second after first 10 seconds
        time_penalty = max(0, completion_seconds - 10)
        self.decay_score = int(time_penalty)
        
        # Final score cannot go below zero
        self.final_score = max(0, self.base_score - self.decay_score)
        
        return self.final_score

