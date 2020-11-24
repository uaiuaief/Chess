import threading
from flask import Flask, render_template, jsonify, request, redirect, url_for
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
            board.move(origin, target, players[ip])
            return 'success', 200
        else:
            return 'fail', 403
    except ValueError:
        # print(ValueError.with_traceback())
        return 'fail', 403


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
    board.reset_board()

    return 'success', 200


@app.route('/api/changes', methods=['GET', 'POST'])
def detect_changes():
    # check_mate, winner = board.check_mate()

    return jsonify(board.info.get_state())

    # return jsonify({
    #     'check': board.check,
    #     'check_mate': check_mate,
    #     'time_up': board.time_up,
    #     'winner': winner,
    #     'move_count': board.move_count,
    #     'turn_count': board.turn_count,
    #     'turn': board.turn,
    #     'last_movement': board.last_movement,
    #     'timer': {
    #         'white': board.timer['white'],
    #         'black': board.timer['black']
    #     },
    #     'history': board.move_history
    # })


@app.route('/api/GET/color')
def get_color():
    ip = request.remote_addr
    return players[ip].color


@app.route('/api/play')
def play_game():
    minutes = int(request.args.get('minutes'))
    board.set_timer(minutes)
    board.info.game_over = False

    return 'success'


def connect():
    ip = request.remote_addr

    if len(players) == 0:
        players[ip] = Player(ip, 'white')
    elif len(players) == 1 and ip not in players:
        players[ip] = Player(ip, 'black')
    else:
        return 'lobby is full'


def clock():
    board.info.clock_is_running = True
    while True:
        if not board.info.game_over:
            time.sleep(0.1)
            board.info.timer[board.info.current_turn] -= 0.1

            if board.info.timer[board.info.current_turn] <= 0:
                board.time_up = 'white' if board.info.current_turn == 'black' else 'black'
                board.game_over = True


def start_clock():
    if not board.info.clock_is_running:
        timer_thread = threading.Thread(target=clock)
        timer_thread.daemon = True
        timer_thread.start()


if __name__ == '__main__':
    app.run(debug=True, port='5500', host='0.0.0.0')
