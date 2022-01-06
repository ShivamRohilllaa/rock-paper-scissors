# Django Import
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from spsapp.models import Player, Result

# Python Import
import random

# Create your views here.

def home(request):
    '''
    homepage and start game logic
    '''
    if request.method=='POST':
        playername = request.POST.get('name')
        if User.objects.filter(username__iexact=playername):
            messages.warning(request, 'This name is already exists, please try another one.')
            return HttpResponseRedirect(request.path_info)
        create_user = User.objects.create(first_name=playername, username=playername)
        create_player = Player.objects.create(name=playername, user=create_user)
        return redirect('start_game')

    return render(request, 'index.html')


def game(request):
    '''
    Rock, paper and scissor logic
    '''
    gamelist = ['rock', 'paper', 'scissors']
    bot_action = random.choice(gamelist)
    user = Player.objects.all().last()

    if request.method == 'POST':
        user_answer = request.POST.get('name')

        if user_answer == bot_action:
            messages.info(request, f"Both players selected {user_answer}. It's a tie!")
            result = Result.objects.create(player=user, bot_move=bot_action, user_move=user_answer, status='Tie')

        elif user_answer == "rock":
            if bot_action == "scissors":
                messages.success(request, "Rock smashes scissors! You win!")
                result = Result.objects.create(player=user, bot_move=bot_action, user_move=user_answer, status='Win')
            else:
                result = Result.objects.create(player=user, bot_move=bot_action, user_move=user_answer, status='Lose')
                messages.info(request, "Paper covers rock! You lose.")

        elif user_answer == "paper":
            if bot_action == "rock":
                messages.success(request, "Paper covers rock! You win!")
                result = Result.objects.create(player=user, bot_move=bot_action, user_move=user_answer, status='Win')
            else:
                result = Result.objects.create(player=user, bot_move=bot_action, user_move=user_answer, status='Lose')
                messages.info(request, "Scissors cuts paper! You lose.")

        elif user_answer == "scissors":
            if bot_action == "paper":
                result = Result.objects.create(player=user, bot_move=bot_action, user_move=user_answer, status='Win')
                messages.success(request, "Scissors cuts paper! You win!")
            else:
                result = Result.objects.create(player=user, bot_move=bot_action, user_move=user_answer, status='Lose')
                messages.info(request, "Rock smashes scissors! You lose.")
    
    return render(request, 'game.html', {'user':user})


def result(request):
    '''
    All users results
    '''
    res = Result.objects.all().order_by('-id')
    context = {'res':res}
    return render(request, 'result.html', context)