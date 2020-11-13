from flask import Flask, render_template, jsonify, request, redirect, url_for
# from main import *
from board import *

app = Flask(__name__)
board = Board()
players = {}


class Player:
    def __init__(self, ip, color):
        self.ip = ip
        self.color = color


@app.route('/')
def index():
    connect()
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

    try:
        ip = request.remote_addr
        if ip in players:
            board.move(origin, target, players[ip])
            return 'success', 200
        else:
            return 'fail', 403
    except ValueError:
        return 'fail', 403


@app.route('/api/reset')
def reset_board():
    board.reset_board()

    return 'success', 200


@app.route('/api/changes', methods=['GET', 'POST'])
def detect_changes():
    check_mate, winner = board.check_mate()
    turn_count = board.turn_count

    return jsonify({
        'check_mate': check_mate,
        'winner': winner,
        'turn_count': turn_count
    })


@app.route('/api/GET/color')
def get_color():
    ip = request.remote_addr
    return players[ip].color


def connect():
    ip = request.remote_addr

    if len(players) == 0:
        players[ip] = Player(ip, 'white')
    elif len(players) == 1:
        players[ip] = Player(ip, 'black')
    else:
        return 'lobby is full'


if __name__ == '__main__':
    app.run(debug=True, port='5500', host='0.0.0.0')
