from flask import Flask, render_template, jsonify, request, redirect, url_for
from main import *

app = Flask(__name__)
board = Board()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/GET/board')
def get_board():
    return jsonify(board.get_state())


@app.route('/api/move', methods=['GET', 'POST'])
def move():
    originx = int(request.args.get('originx'))
    originy = int(request.args.get('originy'))
    targetx = int(request.args.get('targetx'))
    targety = int(request.args.get('targety'))
    origin = [originx, originy]
    target = [targetx, targety]

    print(origin, target)
    try:
        board.move(origin, target)
        return 'success', 200
    except ValueError:
        return 'fail', 403


@app.route('/api/reset')
def reset_board():
    board.reset_board()

    return 'success', 200

if __name__ == '__main__':
    app.run(debug=True, port='5500')
