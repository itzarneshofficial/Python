# Tic-Tac-Toe Game in Python

# Initialize the board
board = [" " for _ in range(9)]

# Function to display the board
def display_board():
    print("-------------")
    for i in range(3):
        print(f"| {board[i * 3]} | {board[i * 3 + 1]} | {board[i * 3 + 2]} |")
        print("-------------")

# Function to check if there is a winner
def check_winner(player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Function to check if the board is full
def is_draw():
    return " " not in board

# Function to handle a player's move
def player_move(player):
    while True:
        try:
            position = int(input(f"Player {player}, choose a position (1-9): ")) - 1
            if position < 0 or position > 8:
                print("Invalid position. Choose a number between 1 and 9.")
            elif board[position] != " ":
                print("Position already taken. Choose another.")
            else:
                board[position] = player
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

# Main function to run the game
def play_game():
    current_player = "X"
    while True:
        display_board()
        player_move(current_player)
        
        if check_winner(current_player):
            display_board()
            print(f"Player {current_player} wins!")
            break
        elif is_draw():
            display_board()
            print("It's a draw!")
            break
        
        # Switch player
        current_player = "O" if current_player == "X" else "X"

# Start the game
play_game()
