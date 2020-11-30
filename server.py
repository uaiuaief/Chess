import time
import threading
import json
from flask import Flask, render_template, jsonify, request, redirect, url_for
from board import *

app = Flask(__name__)
board = Board()
players = {}


class Connections:
    def __init__(self):
        pass


class Player:
    def __init__(self, ip, color):
        self.ip = ip
        self.color = color
        self.connected = False
        self.connection_health = 100


@app.route('/')
def index():
    start_clock()
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
            board.events.move(origin, target, players[ip])
            return 'success', 200
        else:
            raise ValueError('Player is not connected')

    except ValueError as e:
        return str(e), 403


@app.route('/api/promote', methods=['GET', 'POST'])
def promote_pawn():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    promotion = request.args.get('promotion')

    pawn = board.get_piece(x, y)
    pawn.promotion = promotion
    return 'success', 200


@app.route('/api/reset')
def reset_board():
    print(request.remote_addr)
    board.reset_board()

    return 'success', 200


@app.route('/api/changes', methods=['GET', 'POST'])
def detect_changes():
    # print(players[request.remote_addr])
    player = players.get(request.remote_addr)
    if not player:
        return 'Observer'
    player.connection_health = 100
    player.connected = True
    return jsonify(board.info.get_state())


@app.route('/api/GET/color')
def get_color():
    ip = request.remote_addr
    if players.get(ip):
        return players[ip].color
    else:
        return 'Observer has no color'


@app.route('/api/play')
def play_game():
    minutes = int(request.args.get('minutes'))
    board.set_timer(minutes)
    board.info.game_over = False
    board.info.game_started = True

    return 'success'


@app.route('/api/computer')
def play_computer():
    board.info.against_computer = True
    board.info.game_started = True

    return 'success'


def connect():
    ip = request.remote_addr

    if len(players) == 0:
        player = Player(ip, 'white')
        players[ip] = player
        board.info.players.append(player.__dict__)
        player.connected = True
    elif len(players) == 1 and ip not in players:
        player = Player(ip, 'black')
        players[ip] = player
        board.info.players.append(player.__dict__)
        player.connected = True
    else:
        return 'lobby is full'


def clock():
    while True:
        time.sleep(0.1)

        if board.info.against_computer:
            continue

        for player in players:
            # players[player].connection_health -= 1
            players.get(player).connection_health -= 1
            # print(players.get(player).connection_health)

            # print(players[player].connection_health )
            if players.get(player).connection_health == 0:
                players.get(player).connected = False

        if not board.info.game_over:
            board.info.timer[board.info.current_turn] -= 0.1

            if board.info.timer[board.info.current_turn] <= 0:
                board.info.time_up = 'white' if board.info.current_turn == 'black' else 'black'
                board.info.game_over = True


def start_clock():
    if not board.info.clock_is_running:
        board.info.clock_is_running = True
        timer_thread = threading.Thread(target=clock)
        timer_thread.daemon = True
        timer_thread.start()


if __name__ == '__main__':
    app.run(debug=True, port='5500', host='0.0.0.0')
