import streamlit as st
import numpy as np

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2

# Initialize Game Board
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROW_COUNT-1, -1, -1):
        if board[r][col] == EMPTY:
            return r

def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if all(board[r, c+i] == piece for i in range(4)):
                return True
    
    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if all(board[r+i, c] == piece for i in range(4)):
                return True
    
    # Check positive diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+i, c+i] == piece for i in range(4)):
                return True
    
    # Check negative diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i, c+i] == piece for i in range(4)):
                return True
    
    return False

def print_board(board):
    return np.flip(board, 0)

# Streamlit App
st.title("Connect Four Game 🎮")
st.write("### Instructions:")
st.write("1. Player 1 (🔴) and Player 2 (🟡) take turns dropping pieces.")
st.write("2. Click on a column button to drop your piece.")
st.write("3. First to connect **4 in a row** (vertically, horizontally, or diagonally) wins!")
st.write("4. If board is full, it's a **draw**!")

# Session State Initialization
if 'board' not in st.session_state:
    st.session_state.board = create_board()
    st.session_state.turn = PLAYER_ONE
    st.session_state.game_over = False
    st.session_state.message = "Player 1's turn (🔴)"

# Game Grid UI
cols = st.columns(COLUMN_COUNT)
for col in range(COLUMN_COUNT):
    if cols[col].button(f"⬇️ {col+1}", key=col, disabled=st.session_state.game_over):
        if is_valid_location(st.session_state.board, col):
            row = get_next_open_row(st.session_state.board, col)
            drop_piece(st.session_state.board, row, col, st.session_state.turn)
            
            if winning_move(st.session_state.board, st.session_state.turn):
                st.session_state.game_over = True
                st.session_state.message = f"Player {st.session_state.turn} ({'🔴' if st.session_state.turn == PLAYER_ONE else '🟡'}) wins! 🎉"
            else:
                st.session_state.turn = PLAYER_TWO if st.session_state.turn == PLAYER_ONE else PLAYER_ONE
                st.session_state.message = f"Player {st.session_state.turn}'s turn ({'🔴' if st.session_state.turn == PLAYER_ONE else '🟡'})"

# Display Board
game_board = print_board(st.session_state.board)
st.write("### Game Board:")
st.table(game_board)
st.write(st.session_state.message)

# Reset Button
if st.button("Restart Game 🔄"):
    st.session_state.board = create_board()
    st.session_state.turn = PLAYER_ONE
    st.session_state.game_over = False
    st.session_state.message = "Player 1's turn (🔴)"
    st.rerun()  # Correct method to restart the app
