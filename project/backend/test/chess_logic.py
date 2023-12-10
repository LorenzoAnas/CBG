
# 1. Define the Chessboard
class Board:
    def __init__(self):
        self.pieces = [
            [Rook('white', (0, 0)), Knight('white', (0, 1)), Bishop('white', (0, 2)), Queen('white', (0, 3)), King('white', (0, 4)), Bishop('white', (0, 5)), Knight('white', (0, 6)), Rook('white', (0, 7))],
            [Pawn('white', (1, i)) for i in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [Pawn('black', (6, i)) for i in range(8)],
            [Rook('black', (7, 0)), Knight('black', (7, 1)), Bishop('black', (7, 2)), Queen('black', (7, 3)), King('black', (7, 4)), Bishop('black', (7, 5)), Knight('black', (7, 6)), Rook('black', (7, 7))],
        ]

    def is_within_bounds(self, position):
        return 0 <= position[0] < 8 and 0 <= position[1] < 8
    
    def is_empty(self, position):
        return self.pieces[position[0]][position[1]] is None    
    
    def get_piece(self, position):
        return self.pieces[position[0]][position[1]]
    
    def move_piece(self, source, destination):
        # Check if the move is valid
        if not self.is_valid_move(source, destination):
            raise ValueError('Invalid move')
        
        # If the destination is occupied by an enemy piece, capture it
        if not self.is_empty(destination) and self.get_piece(source).color != self.get_piece(destination).color:
            self.pieces[destination[0]][destination[1]] = None

        # Move the piece to the destination
        self.pieces[destination[0]][destination[1]] = self.pieces[source[0]][source[1]]
        self.pieces[source[0]][source[1]] = None

    def is_valid_move(self, source, destination):
        # Check if the source and destination are within bounds
        if not self.is_within_bounds(source) or not self.is_within_bounds(destination):
            return False
        
        # Check if the source and destination are different
        if source == destination:
            return False
        
        # Check if the source is empty
        if self.is_empty(source):
            return False
        
        # Check if the destination is occupied by an enemy piece
        if not self.is_empty(destination) and self.get_piece(source).color != self.get_piece(destination).color:
            return True
        
        # Check if the move is valid for the piece
        if destination not in self.get_piece(source).get_valid_moves(self):
            return False

        return True
    
    def is_checkmate(self, color):
        # Check if the king is in check
        if not self.is_in_check(color):
            return False
        
        # Check if the king can move to a safe square
        king_position = self.get_king_position(color)
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_position = (king_position[0] + dx, king_position[1] + dy)
            
            # If the new position is within bounds and empty, the king can move there
            if self.is_within_bounds(new_position) and self.is_empty(new_position):
                return False
        
        # Check if any friendly piece can capture the attacking piece
        for row in self.pieces:
            for piece in row:
                if piece is not None and piece.color == color:
                    for move in piece.get_valid_moves(self):
                        if self.get_piece(move).color != color:
                            return False
        
        return True
    
    def is_stalemate(self, color):
        # Check if the king is in check
        if self.is_in_check(color):
            return False
        
        # Check if any friendly piece has a valid move
        for row in self.pieces:
            for piece in row:
                if piece is not None and piece.color == color:
                    for move in piece.get_valid_moves(self):
                        if self.is_valid_move(piece.position, move):
                            return False
        
        return True
    
    def is_in_check(self, color):
        # Get the king's position
        king_position = self.get_king_position(color)
        
        # Check if any enemy piece can capture the king
        for row in self.pieces:
            for piece in row:
                if piece is not None and piece.color != color:
                    if king_position in piece.get_valid_moves(self):
                        return True
        
        return False
    
    def get_king_position(self, color):
        # Find the king's position
        for row in self.pieces:
            for piece in row:
                if piece is not None and piece.color == color and isinstance(piece, King):
                    return piece.position
                
        return None
    
    def __str__(self):
        board_str = '   a   b   c   d   e   f   g   h\n'
        board_str += ' +---+---+---+---+---+---+---+---+\n'
        for i, row in enumerate(reversed(self.pieces)):
            board_str += str(8 - i)
            for piece in row:
                if piece is None:
                    board_str += '|   '  # Use '|   ' for empty squares
                else:
                    board_str += '|' + str(piece)[0] + '  '  # Use '|P  ' for a pawn, '|R  ' for a rook, etc.
            board_str += '|\n +---+---+---+---+---+---+---+---+\n'
        return board_str
    
# 2. Define the Chess Pieces
class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
    
    def __str__(self):
        return self.symbol
    
    def get_valid_moves(self, board):
        pass

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        
        if self.color == 'white':
            self.symbol = '♙'
        else:
            self.symbol = '♟︎'
    
    def get_valid_moves(self, board):
        valid_moves = []
        
        # Check the direction of movement
        if self.color == 'white':
            direction = 1
        else:
            direction = -1
        
        # Check if the square in front is empty
        new_position = (self.position[0] + direction, self.position[1])
        if board.is_within_bounds(new_position) and board.is_empty(new_position):
            valid_moves.append(new_position)
            
            # Check if the pawn can move two squares forward
            if self.color == 'white' and self.position[0] == 1:
                new_position = (self.position[0] + 2, self.position[1])
                if board.is_empty(new_position):
                    valid_moves.append(new_position)
            elif self.color == 'black' and self.position[0] == 6:
                new_position = (self.position[0] - 2, self.position[1])
                if board.is_empty(new_position):
                    valid_moves.append(new_position)
        
        # Check if the pawn can capture diagonally
        for dx, dy in [(direction, -1), (direction, 1)]:
            new_position = (self.position[0] + dx, self.position[1] + dy)
            if board.is_within_bounds(new_position):
                piece = board.get_piece(new_position)
                if piece is not None and piece.color != self.color:
                    valid_moves.append(new_position)
        
        return valid_moves
    
    def move(self, new_position):
        # Pawn promotion
        if new_position[0] == 0 or new_position[0] == 7:
            promotion_options = {
                'queen': Queen,
                'rook': Rook,
                'bishop': Bishop,
                'knight': Knight
            }
            
            # Let the user choose the piece to promote
            promotion_choice = input("Choose a piece to promote (queen, rook, bishop, knight): ")
            
            # Get the corresponding piece class from the dictionary
            promotion_piece = promotion_options.get(promotion_choice.lower())
            
            if promotion_piece:
                # Create a new instance of the chosen piece class
                promoted_piece = promotion_piece(self.color, new_position)
                
                # Replace the pawn with the promoted piece
                self = promoted_piece
            else:
                print("Invalid promotion choice.")
            
        # Normal move
        self.position = new_position
        return self
    
class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        
        if self.color == 'white':
            self.symbol = '♖'
        else:
            self.symbol = '♜'
    
    def get_valid_moves(self, board):
        valid_moves = []
        
        # Check each direction: up, down, left, right
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for distance in range(1, 8):
                new_position = (self.position[0] + dx * distance, self.position[1] + dy * distance)
                
                # If the new position is within bounds and empty, the rook can move there
                if board.is_within_bounds(new_position):
                    valid_moves.append(new_position)
                else:
                    break
        
        return valid_moves
    
    def move(self, new_position):
        self.position = new_position
        return self
    
class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        
        if self.color == 'white':
            self.symbol = '♔'
        else:
            self.symbol = '♚'
    
    def get_valid_moves(self, board):
        valid_moves = []
        
        # Check each direction: up, down, left, right, and the four diagonals
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_position = (self.position[0] + dx, self.position[1] + dy)
            
            # If the new position is within bounds and either empty or occupied by an enemy piece, the king can move there
            if board.is_within_bounds(new_position):
                piece = board.get_piece(new_position)
                if piece is not None and piece.color != self.color:
                    valid_moves.append(new_position)
        
        return valid_moves
    
    def move(self, new_position):
        self.position = new_position
        return self
    
class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        
        if self.color == 'white':
            self.symbol = '♕'
        else:
            self.symbol = '♛'
    
    def get_valid_moves(self, board):
        valid_moves = []
        
        # Check each direction: up, down, left, right, and the four diagonals
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            for distance in range(1, 8):
                new_position = (self.position[0] + dx * distance, self.position[1] + dy * distance)
                
                # If the new position is within bounds and empty, the queen can move there
                if board.is_within_bounds(new_position):
                    valid_moves.append(new_position)
                else:
                    break
        
        return valid_moves
    
    def move(self, new_position):
        self.position = new_position
        return self
    
class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        
        if self.color == 'white':
            self.symbol = '♗'
        else:
            self.symbol = '♝'
    
    def get_valid_moves(self, board):
        valid_moves = []
        
        # Check each direction: the four diagonals
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            for distance in range(1, 8):
                new_position = (self.position[0] + dx * distance, self.position[1] + dy * distance)
                
                # If the new position is within bounds and empty, the bishop can move there
                if board.is_within_bounds(new_position):
                    valid_moves.append(new_position)
                else:
                    break
        
        return valid_moves
    
    def move(self, new_position):
        self.position = new_position
        return self
    
class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        
        if self.color == 'white':
            self.symbol = '♘'
        else:
            self.symbol = '♞'
    
    def get_valid_moves(self, board):
        valid_moves = []
        
        # Check each direction: up, down, left, right, and the four diagonals
        for dx, dy in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            new_position = (self.position[0] + dx, self.position[1] + dy)
            
            # If the new position is within bounds and either empty or occupied by an enemy piece, the knight can move there
            if board.is_within_bounds(new_position):
                piece = board.get_piece(new_position)
                if piece is not None and piece.color != self.color:
                    valid_moves.append(new_position)
        
        return valid_moves
    
    def move(self, new_position):
        self.position = new_position
        return self
    
# 3. Implement the Game Loop
class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_player = 'white'
    
    def make_move(self, source, destination):
        # Check if the move is valid
        if not self.board.is_valid_move(source, destination):
            raise ValueError('Invalid move')
        
        # Move the piece
        self.board.move_piece(source, destination)
        
        # Switch players
        if self.current_player == 'white':
            self.current_player = 'black'
        else:
            self.current_player = 'white'
    
    def check_game_over(self):
        # Check for checkmate or stalemate
        if self.board.is_checkmate(self.current_player) or self.board.is_stalemate(self.current_player):
            return True
        
        return False
    
    def __str__(self):
        return str(self.board)
    
# 4. Implement the User Interface
def get_user_input():
    # Get the user's input, while explaining how to enter a move making an example move
    move = input('Enter a move (e.g. "a2-a4"): ')
    
    # Parse the input
    source, destination = move.split('-')
    source = (int(source[1]) - 1, ord(source[0]) - ord('a'))
    destination = (int(destination[1]) - 1, ord(destination[0]) - ord('a'))
    
    return source, destination

# 5. Integrate with Django, React, and PostgreSQL
# 6. Test the Chess Game
def main():
    # Initialize the game
    game = ChessGame()
    
    # Display the chessboard
    print(game)
    
    # Game loop
    while True:
        # Get the user's move
        source, destination = get_user_input()
        
        # Make the move
        try:
            game.make_move(source, destination)
        except ValueError:
            print('Invalid move')
            continue
        
        # Display the chessboard
        print(game)
        
        # Check for checkmate or stalemate
        if game.check_game_over():
            print('Game over')
            break

if __name__ == '__main__':
    main()


