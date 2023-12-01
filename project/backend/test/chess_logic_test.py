class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def move(self, new_position):
        self.position = new_position

    def get_valid_moves(self, board):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__

class Pawn(Piece):
    def get_valid_moves(self, board):
        direction = 1 if self.color == 'white' else -1
        start_row = 1 if self.color == 'white' else 6
        valid_moves = []

        # Move forward
        forward_square = (self.position[0] + direction, self.position[1])
        if board.is_empty(forward_square):
            valid_moves.append(forward_square)

            # Double move from start
            double_forward_square = (self.position[0] + 2 * direction, self.position[1])
            if self.position[0] == start_row and board.is_empty(double_forward_square):
                valid_moves.append(double_forward_square)

        # Capture
        for dx in [-1, 1]:
            capture_square = (self.position[0] + direction, self.position[1] + dx)
            if board.is_within_bounds(capture_square) and not board.is_empty(capture_square) and board.get_piece(capture_square).color != self.color:
                valid_moves.append(capture_square)

            # En passant
            side_square = (self.position[0], self.position[1] + dx)
            if board.is_within_bounds(side_square) and not board.is_empty(side_square) and board.get_piece(side_square).color != self.color and board.get_piece(side_square).just_double_moved:
                valid_moves.append(capture_square)

        return valid_moves

    def move(self, new_position):
        # Pawn promotion
        if new_position[0] == 0 or new_position[0] == 7:
            return Rook(self.color, new_position) # Need to add logic to let the user choose!

        # Normal move
        self.position = new_position
        return self
    
class Rook(Piece):
    def get_valid_moves(self, board):
        valid_moves = []

        # Check each direction: up, down, left, right
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for distance in range(1, 8):
                new_position = (self.position[0] + dx * distance, self.position[1] + dy * distance)

                # Stop if the new position is out of bounds
                if not board.is_within_bounds(new_position):
                    break

                # If the square is empty, add it to the valid moves
                if board.is_empty(new_position):
                    valid_moves.append(new_position)
                else:
                    # If the square is occupied by an enemy piece, add it to the valid moves and stop
                    if board.get_piece(new_position).color != self.color:
                        valid_moves.append(new_position)
                    break

        return valid_moves

class King(Piece):
    def get_valid_moves(self, board):
        valid_moves = []

        # Check each direction: up, down, left, right, and the four diagonals
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_position = (self.position[0] + dx, self.position[1] + dy)

            # If the new position is within bounds and either empty or occupied by an enemy piece, add it to the valid moves
            if board.is_within_bounds(new_position) and (board.is_empty(new_position) or board.get_piece(new_position).color != self.color):
                valid_moves.append(new_position)

        return valid_moves

class Board:
    def __init__(self):
        self.pieces = [
            [Rook('white', (0, 0)), None, None, None, None, None, None, Rook('white', (0, 7))],
            [Pawn('white', (1, i)) for i in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [Pawn('black', (6, i)) for i in range(8)],
            [Rook('black', (7, 0)), None, None, None, None, None, None, Rook('black', (7, 7))],
        ]

    def is_within_bounds(self, position):
        return 0 <= position[0] < 8 and 0 <= position[1] < 8

    def is_empty(self, position):
        return self.pieces[position[0]][position[1]] is None

    def get_piece(self, position):
        return self.pieces[position[0]][position[1]]

    def move(self, piece, new_position):
        # Check if the move is valid
        if new_position not in piece.get_valid_moves(self):
            raise ValueError('Invalid move')

        # Clear the starting cell
        self.pieces[piece.position[0]][piece.position[1]] = None

        # Make the move
        piece.move(new_position)

        # Update the board state
        self.pieces[new_position[0]][new_position[1]] = piece

    def __str__(self):
        board_str = '  a b c d e f g h\n'
        for i, row in enumerate(reversed(self.pieces)):
            board_str += str(8 - i) + ' '
            for piece in row:
                if piece is None:
                    board_str += '. '
                else:
                    board_str += str(piece)[0] + ' '  # Use the first character of the piece's name
            board_str += '\n'
        return board_str


class Game:
    def __init__(self):
        self.board = Board()

    def play(self):
        while True:
            # Print the board
            print(self.board)

            # Get the move from the user
            move = input('Enter your move: ')

            # Parse the move
            piece_position, new_position = move.split('-')
            piece = self.board.get_piece((int(piece_position[0]) - 1, int(piece_position[1]) - 1))

            # Make the move
            self.board.move(piece, (int(new_position[0]) - 1, int(new_position[1]) - 1))

game = Game()
game.play()