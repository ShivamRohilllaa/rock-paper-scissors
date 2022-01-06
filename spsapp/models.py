from django.db import models
from django.contrib.auth.models import User
from django.db.models.lookups import Range

# Create your models here.

class Game(models.Model):
    '''
    Game model with choices Rock, Paper and Scissor
    '''        
    Rock = 'Rock'
    Paper = 'Paper'
    Scissors = 'Scissors'
    GAME_CHOICES = [
        (Rock, 'Rock'),
        (Paper, 'Paper'),
        (Scissors, 'Scissors'),
    ]
    game_choices = models.CharField(max_length=10, choices=GAME_CHOICES)


class Player(models.Model):
    '''
    Player model 
    '''
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='player_game')

    def __str__(self):
        return self.name


class Result(models.Model):
    '''
    Result model in which all players result will be stored
    '''
    player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name='score')
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='game_score')
    score = models.IntegerField()

    def __str__(self):
        return 'score -- ' + self.score + ' by ' + self.player.name

