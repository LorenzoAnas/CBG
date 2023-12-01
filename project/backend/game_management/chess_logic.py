class ChessLogic:
    @staticmethod
    def make_move(board_state, move):
        # Parse the move
        source, destination = move.split('-')

        # Check if the move is valid
        if not ChessLogic.is_valid_move(board_state, source, destination):
            raise ValueError('Invalid move')

        # Make the move
        piece = board_state[source]
        board_state[source] = None
        board_state[destination] = piece

        return board_state

    @staticmethod
    def is_valid_move(board_state, source, destination):
        # This is just a placeholder
        return True  # Replace with actual logic

    @staticmethod
    def check_game_over(board_state):
        # Check for checkmate or stalemate
        if ChessLogic.is_checkmate(board_state) or ChessLogic.is_stalemate(board_state):
            return True

        return False

    @staticmethod
    def is_checkmate(board_state):
        # This is just a placeholder
        return False  # Replace with actual logic

    @staticmethod
    def is_stalemate(board_state):
        # This is just a placeholder
        return False  # Replace with actual logic