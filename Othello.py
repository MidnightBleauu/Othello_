# Author: Pramit Patel
# GitHub username: midnightbleau or SsunsetHorions (Both of which are mine)
# Date: 06/11/23
# Description: For this project we're creating a text-based game of Othello

class Player:
    """ Represents the players in the Othello game """

    def __init__(self, name, color):
        self._name = name
        self._color = color


def valid_position(x, y):
    """A helper method that represents if the position is valid and returns it """

    return 1 <= x <= 8 and 1 <= y <= 8


class Othello:
    """ Represents the othello game """

    def __init__(self):
        self._board = []

        for i in range(10):         # Creates a 10 x 10 board
            row = []
            for j in range(10):
                if i == 0 or i == 9 or j == 0 or j == 9:  # Ensures game is played on 8X8 grid
                    row.append("*")
                else:
                    row.append(".")
            self._board.append(row)

        self._board[4][4] = self._board[5][5] = "O"  # places initial  pieces on the board
        self._board[4][5] = self._board[5][4] = "X"  # same as above
        self._players = []

    def print_board(self):
        """Represents a method to print out board, and current piece location"""

        for row in self._board:
            print(" ".join(row))
        print()

    def create_player(self, player_name, color):
        """Method that creates a player object with name and color """

        create_new_player = Player(player_name, color)   # Creates new player with black, and white colors
        self._players.append(create_new_player)

    def return_winner(self):
        """ Method that returns the winner and if its a tie. """

        player_white_pieces = sum(row.count("O") for row in self._board)
        player_black_pieces = sum(row.count("X") for row in self._board)

        # Looks for player object based on player color
        player_white = [player for player in self._players if player._color == "white"][0]
        player_black = [player for player in self._players if player._color == "black"][0]

        if player_white_pieces > player_black_pieces:   # determines winners by comparing number of pieces
            return "Winner is white player: " + player_white._name
        elif player_black_pieces > player_white_pieces:
            return "Winner is black player: " + player_black._name
        else:
            return "It's a tie"

    def return_available_positions(self, color):
        """ Method that puts a piece of the specified color at the given position and updates it"""

        player_color = "X" if color == "black" else "O"
        opponent_color = "O" if player_color == "white" else "X"
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        available_positions = []

        for i in range(1, 9):
            for j in range(1, 9):
                if self._board[i][j] == '.':
                    for direction in directions:
                        x, y = i + direction[0], j + direction[1]
                        if 1 <= x <= 8 and 1 <= y <= 8 and self._board[x][y] == opponent_color:
                            while 1 <= x <= 8 and 1 <= y <= 8:
                                if self._board[x][y] == player_color:
                                    available_positions.append((i, j))
                                    break
                                elif self._board[x][y] == '.' or self._board[x][y] == '*':
                                    break
                                x += direction[0]
                                y += direction[1]

        return sorted(available_positions)

    def make_move(self, color, piece_position):
        """ puts a piece of the specified color at the given position and updates the board accordingly,"""

        player_colors = "X" if color == "black" else "O"
        all_directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

        self._board[piece_position[0]][piece_position[1]] = color # puts the pieces at the positon

        for direction in all_directions:    # checks for the direction for swapping pieces
            x, y = piece_position[0] + direction[0], piece_position[1] + direction[1]
            swap_pieces = []

            while valid_position(x, y) and self._board[x][y] == player_colors:
                swap_pieces.append((x, y))
                x += direction[0]
                y += direction[1]

                if swap_pieces and valid_position(x, y) and self._board[x][y] == color:
                    for x, y in swap_pieces:  # swaps the opponents pieces to teh player's color
                        self._board[x][y] = color

            return self._board

    def play_game(self, player_color, piece_position):
        """A method that plays teh game via making a move for the player"""

        player_colors = "X" if player_color == "black" else "O"
        available_positions = self.return_available_positions(player_color)

        if piece_position not in available_positions:
            print("Invalid Move. Valid moves are:")
            for move in available_positions:
                print(move)
            return "Invalid Move!"
        else:
            print("Valid moves are:")
            for move in available_positions:
                print(move)

            self.make_move(player_colors, piece_position)

            white_pieces = sum(row.count("O") for row in self._board)
            black_pieces = sum(row.count("X") for row in self._board)

            if white_pieces + black_pieces == 64 or len(self.return_available_positions("white")) == 0 and len(
                    self.return_available_positions("black")) == 0:
                print(f"Game ended: White pieces: {white_pieces}, Black pieces: {black_pieces}")
                return self.return_winner()

