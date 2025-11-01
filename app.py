from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from base import db
from tables import User
from dotenv import load_dotenv
import os
import random
import copy

# Justing the .env variables and collecting
load_dotenv()

user_db = os.getenv('user_db')
user_password = os.getenv('user_pass')
port = os.getenv('port')
host = os.getenv('host')
db_name = os.getenv('db_name')

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)




# ==================
# TETROMINOS & HELPERS
# ==================
TETROMINOS = {
    "I": [[1,1,1,1]],
    "O": [[1,1],[1,1]],
    "T": [[0,1,0],[1,1,1]],
    "S": [[0,1,1],[1,1,0]],
    "Z": [[1,1,0],[0,1,1]],
    "J": [[1,0,0],[1,1,1]],
    "L": [[0,0,1],[1,1,1]]
}

def new_piece():
    shape = random.choice(list(TETROMINOS.values()))
    return {"shape": shape, "x": 3, "y": 0}

def empty_board():
    return [[0]*10 for _ in range(20)]

def valid_position(board, piece, offset_x=0, offset_y=0):
    for y, row in enumerate(piece["shape"]):
        for x, cell in enumerate(row):
            if cell:
                new_x = piece["x"] + x + offset_x
                new_y = piece["y"] + y + offset_y
                if new_x < 0 or new_x >= 10 or new_y >= 20:
                    return False
                if new_y >= 0 and board[new_y][new_x]:
                    return False
    return True

def place_piece(board, piece):
    for y, row in enumerate(piece["shape"]):
        for x, cell in enumerate(row):
            if cell and 0 <= piece["y"] + y < 20:
                board[piece["y"] + y][piece["x"] + x] = 1

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = 20 - len(new_board)
    while len(new_board) < 20:
        new_board.insert(0, [0]*10)
    return new_board, lines_cleared

def rotate(piece):
    piece["shape"] = [list(row) for row in zip(*piece["shape"][::-1])]

# ==================
# AUTH ROUTES
# ==================
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        form = request.form.to_dict()
        email = form.get('email')
        username = form.get('username')

        if User.query.filter_by(email=email).first():
            return jsonify({'status':'error','message':'Usuário já cadastrado'})
        if User.query.filter_by(username=username).first():
            return jsonify({'status':'error','message':'Nome de usuário não disponível'})

        password = generate_password_hash(form.get('password'))
        new_user = User(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'status':'success'})

    return render_template('signup.html')

@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        form = request.form.to_dict()
        user = User.query.filter_by(email=form.get('email')).first()
        if not user or not check_password_hash(user.password, form.get('password')):
            return jsonify({'status':'error','message':'Credenciais Inválidas'})
        return jsonify({'status':'success'})
    return render_template('index.html')

@app.route('/main')
def main_page():
    return render_template('main.html')

# ==================
# TETRIS ROUTES
# ==================
@app.route('/start', methods=['POST'])
def start_tetris():
    board = empty_board()
    piece = new_piece()
    session['board'] = board
    session['piece'] = piece
    session['game_over'] = False
    return jsonify({'board': board, 'piece': piece})

@app.route('/move', methods=['POST'])
def move_tetris():
    if session.get('game_over', False):
        return jsonify({'status':'game_over'})

    data = request.get_json()
    direction = data.get('direction')
    board = session.get('board', empty_board())
    piece = session.get('piece', new_piece())

    piece_copy = copy.deepcopy(piece)

    if direction == 'left' and valid_position(board, piece_copy, offset_x=-1):
        piece_copy['x'] -= 1
    elif direction == 'right' and valid_position(board, piece_copy, offset_x=1):
        piece_copy['x'] += 1
    elif direction == 'down':
        if valid_position(board, piece_copy, offset_y=1):
            piece_copy['y'] += 1
        else:
            place_piece(board, piece_copy)
            board, _ = clear_lines(board)
            piece_copy = new_piece()
            if not valid_position(board, piece_copy):
                session['game_over'] = True
                session['board'] = board
                return jsonify({'status':'game_over','board':board})
    elif direction == 'rotate':
        rotate(piece_copy)
        if not valid_position(board, piece_copy):
            # undo rotation
            for _ in range(3):
                rotate(piece_copy)

    session['piece'] = piece_copy
    session['board'] = board

    return jsonify({'board': board, 'piece': piece_copy})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)