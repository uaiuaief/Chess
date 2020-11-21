import { Board } from './board.js';
import { Screen } from './screen.js';
import { Controller } from './controller.js';


window.turn_count = 1
class ServerCommunication {
    time_up_handled = false;
    tenseconds_warning_played = false;

    handleCheckMate(data) {
        $('.end-game-text').text('Check Mate')
        $('.winner').text(`${data.winner} wins`)
        $('#check-mate').show();
        audio.game_end.play();
    }

    handleTimeUp(data) {
        if (!this.time_up_handled) {
            $('.end-game-text').text(`Time's up`)
            $('.winner').text(`${data.time_up} wins`)
            $('#check-mate').show();
            audio.game_end.play();
            this.time_up_handled = true;
        }
    }

    handleTurnChange(data) {
        if (turn == player_color) {
            $('.self-timer').addClass("active")
            $('.enemy-timer').removeClass("active")
        }
        else {
            $('.enemy-timer').addClass("active")
            $('.self-timer').removeClass("active")
        }
        turn_count = data.turn_count;
        getBoard();

        if (data.check_mate) {
            this.handleCheckMate(data)
        }
    }

    handleTimer(data) {
        let player_date = new Date(0);
        player_date.setSeconds(data.timer[player_color]);
        var player_timer = player_date.toISOString().substr(14, 5);

        let enemy_date = new Date(0);
        enemy_date.setSeconds(data.timer[enemy_color]);
        var enemy_timer = enemy_date.toISOString().substr(14, 5);

        $('.self-timer').text(player_timer)
        $('.enemy-timer').text(enemy_timer)
        turn = data.turn;

        if (!this.tenseconds_warning_played && data.timer[player_color] <= 11) {
            audio.tenseconds.play()
            this.tenseconds_warning_played = true;
        }
    }

    detectChanges() {
        fetch(`/api/changes`)
            .then((res) => res.json()
                .then(data => {
                    this.handleTimer(data);

                    if (turn_count != data.turn_count) {
                        this.handleTurnChange(data);
                        if (turn == player_color)  {
                            audio.move_opponent.play();
                        }
                    }
                    if (data.time_up) {
                        this.handleTimeUp(data);
                    }

                    if (data.last_movement) {
                        if (player_color == 'black') {
                            let [ox, oy] = data.last_movement[0];
                            let [tx, ty] = data.last_movement[1];
                            [ox, oy] = [7-ox, 7-oy];
                            [tx, ty] = [7-tx, 7-ty];
                            window.last_movement = [[ox, oy], [tx, ty]];
                        }
                        else {
                            window.last_movement = [data.last_movement[0], data.last_movement[1]]
                        }
                    }
                    else {
                        window.last_movement = null;
                    }
                })
            )
    }
}

class Mouse {
    constructor() {
        this.x
        this.y
        $(window).on('mousemove', (e) => this.move(e))
        $('canvas').on('mousedown', (e) => this.b1_down(e))
    }

    getCoord() {
        return [this.x, this.y]
    }

    setCoord(x, y) {
        this.x = x;
        this.y = y;
    }

    getIndex() {
        let i = Math.floor(this.x / 80);
        let j = Math.floor(this.y / 80);

        return [i, j]
    }

    move(event) {
        let rect = canvas.getBoundingClientRect();
        let x = event.clientX - rect.left;
        let y = event.clientY - rect.top;

        this.setCoord(x, y)
    }

    b1_down(event) {
        if (event.originalEvent.button == 0) {
            window.controller.mouseDown(event)
        }
    }
}

class AudioPlayer {
    capture = new Audio('/static/audio/capture.wav')
    move_self = new Audio('/static/audio/move-self.wav')
    move_opponent = new Audio('/static/audio/move-opponent.wav')
    illegal = new Audio('/static/audio/illegal.wav')
    game_end = new Audio('/static/audio/game-end.wav')
    game_start = new Audio('/static/audio/game-start.wav')
    move_check = new Audio('/static/audio/move-check.wav')
    promote = new Audio('/static/audio/promote.wav')
    tenseconds = new Audio('/static/audio/tenseconds.wav')
    premove = new Audio('/static/audio/premove.wav')
    castle = new Audio('/static/audio/castle.wav')

}

window.audio = new AudioPlayer;
window.mouse = new Mouse();
window.server_comm = new ServerCommunication()

window.canvas = document.getElementById("canvas");
window.ctx = canvas.getContext("2d");
window.bg_canvas = document.getElementById("background-canvas")
window.bg_ctx = bg_canvas.getContext("2d");
window.basis = 80;
window.width = basis * 8;
window.height = basis * 8;

window.getBoard = getBoard;
window.player_color = null;
window.enemy_color = null;
window.turn = 'white';
window.last_movement = null;

async function loadEverything() {
    window.board_state = fetch('/api/GET/board')
    window.board = new Board();
    window.screen = new Screen();
    window.controller = new Controller();
    window.canvasElem = document.querySelector("canvas");
    window.moveRequest = {}

    fetch('/api/GET/color')
        .then(res => {
            res.text().then(color => {
                window.player_color = color
                enemy_color = color == 'white' ? 'black' : 'white'

                if (turn == player_color) {
                    $('.self-timer').addClass("active")
                    $('.enemy-timer').removeClass("active")
                }
            })
            // res.text().then(color => {
            //     window.player_color = 'black'
            //     // enemy_color = color == 'white' ? 'black' : 'white'
            //     enemy_color = 'white'
            // })

        })

    window.sprite_list = loadSprites()

}

loadEverything().then(() => getBoard())

async function getBoard() {
    board_state = await fetch('/api/GET/board');
    await board.loadPieces();
    if (player_color == 'black') {
        board.invert()
    }
    screen.drawBackground();
}


function loadSprites() {
    let sprite_list = []
    let names = ['pawn', 'bishop', 'knight', 'rook', 'king', 'queen'];
    let colors = ['white', 'black'];
    names.forEach(name => {
        colors.forEach(color => {
            window.sprite = new Image();
            sprite.src = `static/icons/${color}_${name}.svg`
            sprite_list[`${color}_${name}`] = sprite
        })
    })
    return sprite_list
}

function resetBoard() {
    fetch('/api/reset').then(() => {
        getBoard();
    })
}

$('#reset').on('click', () => resetBoard())
$('.restart').on('click', () => {
    resetBoard()
    $('#check-mate').hide();
    audio.game_start.play()
    server_comm.time_up_handled = false;
    server_comm.tenseconds_warning_played = false;
})


setInterval(() => {
    server_comm.detectChanges(turn_count)
}, 500);

requestAnimationFrame(() => {
    screen.drawBoard()

})





