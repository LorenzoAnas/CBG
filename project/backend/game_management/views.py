from django.shortcuts import render

# Create your views here.
# game_management/views.py
from django.http import JsonResponse
from .models import ChessGame
from .chess_logic import ChessLogic

def make_move(request, game_id):
    # This view expects a POST request with a 'move' parameter

    # Retrieve the game instance
    game = ChessGame.objects.get(pk=game_id)

    if game.is_game_over:
        return JsonResponse({'message': 'Game is already over.'}, status=400)

    # Get the move from the request
    move = request.POST.get('move')
    if move is None:
        return JsonResponse({'message': 'No move provided.'}, status=400)

    # Make the move using your game logic
    game.board_state = ChessLogic.make_move(game.board_state, move)
    game.is_game_over = ChessLogic.check_game_over(game.board_state)
    game.save()

    return JsonResponse({'board_state': game.board_state, 'is_game_over': game.is_game_over})
