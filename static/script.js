import { Board } from './board.js';
import { Screen } from './screen.js';
import { Controller } from './controller.js';
import { HUD } from './HUD.js';
import { AudioPlayer } from './audio_player.js';
import { Mouse } from './mouse.js';
import { ServerCommunication } from './server_communication.js';

class MainLoop {
    constructor(){
        this.running_functions = [];
    }

    run() {
        setInterval(() => {
            this.running_functions.forEach(func => func())
        }, 1000);
    }

    addFunction(func) {
        this.running_functions.push(func);
    }
}


window.move_count = 0;
window.turn_count = 1;

window.audio = new AudioPlayer;
window.mouse = new Mouse();
window.loop = new MainLoop();
window.server_comm = new ServerCommunication()

window.hud = new HUD();

window.canvas = document.getElementById("canvas");
window.ctx = canvas.getContext("2d");
window.bg_canvas = document.getElementById("background-canvas")
window.bg_ctx = bg_canvas.getContext("2d");
window.basis = 80;
window.width = basis * 8;
window.height = basis * 8;

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


                if (player_color == 'white') {
                    $('.captured-pieces.self p span').addClass('captured-black');
                    $('.captured-pieces.enemy p span').addClass('captured-white')
                }
                else {
                    $('.captured-pieces.self p span').addClass('captured-white');
                    $('.captured-pieces.enemy p span').addClass('captured-black')
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

loadEverything().then(() => {
    server_comm.getBoard()
})


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


loop.addFunction(() => server_comm.detectChanges());
loop.run()

window.onload = () => {
    // console.log(server_comm.server_info);
}

// setInterval(() => {
//     server_comm.detectChanges()

// }, 1000);

requestAnimationFrame(() => {
    screen.drawBoard();

})




