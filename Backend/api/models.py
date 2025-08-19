from django.db import models
import string, random
from django.core.exceptions import ValidationError
from .utils import GetQ   # import your question generator
import json

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase, k=10))


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_code = models.CharField(max_length=10, unique=True, default=generate_room_code, editable=False)
    max_players = models.PositiveIntegerField(default=4)
    is_adult = models.BooleanField(default=False)  # 18+ questions toggle
    created_at = models.DateTimeField(auto_now_add=True)
    questions = models.JSONField(default=list)  
    
    def save(self, *args, **kwargs):
        # generate questions only when room is first created
        if not self.pk and not self.questions:
            gen = GetQ()
            raw = gen.get(X=10, Y=2)  # you can tune X, Y dynamically
            try:
                self.questions = json.loads(raw)
            except Exception:
                self.questions = []  # fallback if Gemini response breaks
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.room_code}"



class Player(models.Model):
    username = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="players", null=True, blank=True)
    is_host = models.BooleanField(default=False)

    def clean(self):
        if self.room:
            # prevent overfilling
            if self.room.players.count() >= self.room.max_players and not self.pk:
                raise ValidationError("This room is already full.")

    def save(self, *args, **kwargs):
        # assign host automatically if first player in room
        if self.room and not self.pk and self.room.players.count() == 0:
            self.is_host = True
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        room = self.room
        is_host = self.is_host
        super().delete(*args, **kwargs)

        # if host left, promote another player to host
        if room and is_host:
            next_player = room.players.first()
            if next_player:
                next_player.is_host = True
                next_player.save()

    def __str__(self):
        return f"{self.username} ({'Host' if self.is_host else 'Player'})"

