from django.db import models

class ChessGame(models.Model):
    # A simple representation of the board state as a string.
    # Each piece can be represented by a letter, and empty squares by a dot "."
    # This is a simplified example; a better approach would be to store moves and compute the board.
    board_state = models.TextField(default="RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr")
    turn = models.CharField(max_length=1, default='W')  # 'W' for white, 'B' for black
    is_game_over = models.BooleanField(default=False)
    # Add any additional fields you want

    def __str__(self):
        return f"ChessGame #{self.id}"