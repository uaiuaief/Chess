let game_variables = {
    'selected_square': null,
    'click_one': null,
    'click_two': null,
    'mouse_position': null,
    'dragged_piece': null,
    'reponse': null,

}


class Screen {
    constructor() {
        this.drawBackground();
    }

    // async getPieces(){
    //     let piece_list = [];
    //     let res_clone = await board_promise;

    //     data.map(each => {
    //         piece_list.push(new Piece(each.name, each.color, [each.x, each.y]))            
    //     })

    //     return piece_list;
    // }

    // async findPiece(i, j){
    //     let piece_list = await this.getPieces();
    //     let piece;
    //     piece_list.some(each => {
    //         let same_row = (each.x == i);
    //         let same_column = (each.y == j);
    //         if (same_row && same_column){
    //             return piece;
    //         }
    //     })
    // }

    async drawBoard() {
        ctx.clearRect(0, 0, width, height)
        // this.drawSquares();
        this.highlightSquare();
        this.drawAllPieces();
        // this.drawNumbers();
        // this.drawLetters();
        this.showPossibleMoves();

        // this._dragPiece()

    }

    drawBackground(){
        this.drawSquares();
        this.drawNumbers();
        this.drawLetters();
    }

    async drawAllPieces() {
        let res = await board_promise;
        let data = await res.json();
        
        data.map((each) => this.drawPiece(each))
    }

    async drawPiece(piece) {
        let posX = piece.x * basis
        let posY = piece.y * basis
        ctx.drawImage(sprite_list[`${piece.color}_${piece.name}`], posX, posY)
    }



// TODO

    //  async _dragPiece() {
    //     if (game_variables['selected_square']){
    //         let [i, j] = game_variables['selected_square'];
    //         let piece = await this.findPiece(i, j)
    //         console.log(piece);

    //         // if (game_variables['mouse_position']) {
    //         //     let [x, y] = game_variables['mouse_position'];
    //         //     piece.context.drawImage(sprite_list[`${piece.color}_${piece.name}`], x, y)
    //         //     // ctx.fillStyle = "red";
    //         //     // ctx.fillRect(x, y, 80, 80);

    //         // }
    //     }
    // }

    // async _drawAllPieces() {
    //     let pieces = await this.getPieces();
    //     pieces.map(each => this._drawPiece(each))

    // }

    // _drawPiece(piece) {
    //     let posX = piece.x * basis
    //     let posY = piece.y * basis
    //     piece.context.drawImage(sprite_list[`${piece.color}_${piece.name}`], posX, posY)
    // }




    drawSquares() {
        bg_ctx.fillStyle = '#eeeed4';
        bg_ctx.fillRect(-1, 0, width, height)
        bg_ctx.fillStyle = '#6d945d';

        for (let i = -1; i < 8; i++) {
            for (let j = -1; j < 8; j++) {
                if (i % 2 == 1) {
                    if (j % 2 == 0) {
                        bg_ctx.fillRect(j * basis, i * basis, basis, basis);
                    }
                }
                else {
                    if (j % 2 == 1) {
                        bg_ctx.fillRect(j * basis, i * basis, basis, basis);
                    }
                }
            }
        }

    }

    drawNumbers() {
        for (let i = 0; i <= 8; i++) {
            let isPair = i % 2 == 0
            if (!isPair) {
                bg_ctx.fillStyle = '#eeeed4'
            } else {
                bg_ctx.fillStyle = '#6d945d'
            }
            bg_ctx.font = 'bold 17px Arial'
            bg_ctx.fillText(i, 2, 657 - (i * basis))
        }
    }

    drawLetters() {
        let letters = 'abcdefgh'
        for (let i = 0; i <= 8; i++) {
            let isPair = i % 2 == 0
            if (isPair) {
                bg_ctx.fillStyle = '#eeeed4'
            } else {
                bg_ctx.fillStyle = '#6d945d'
            }
            bg_ctx.font = 'bold 17px Arial'
            bg_ctx.fillText(letters[i], (i * basis) + 64, 635)
        }
    }

    drawSmallCircle(i, j) {
        let posX = (i * basis) + 39
        let posY = (j * basis) + 39
        ctx.fillStyle = 'rgba(-1, 0, 0, .2)';
        ctx.beginPath();
        ctx.arc(posX, posY, 9, 0, 2 * Math.PI);
        ctx.fill()

    }

    drawCaptureSquare(i, j) {
        ctx.strokeStyle = 'rgba(254, 0, 0, .5)';
        ctx.lineWidth = '3';
        ctx.beginPath();
        ctx.rect(i * basis, j * basis, basis, basis);
        ctx.stroke();

    }

    async showPossibleMoves() {
        let selected_square = game_variables['selected_square'];
        if (selected_square) {
            let piece = await getPiece(selected_square[0], selected_square[1])
            let moves = piece.moves;
            if (moves) {
                moves.map(async move => {
                    let enemy_piece = await getPiece(move.x, move.y);
                    if (enemy_piece) {
                        this.drawCaptureSquare(move.x, move.y)
                    }
                    else {
                        this.drawSmallCircle(move.x, move.y);
                    }
                })
            }
        }
    }

    highlightSquare() {
        let selected_square = game_variables['selected_square']
        if (selected_square != null) {
            let [i, j] = selected_square;
            ctx.fillStyle = 'rgba(248, 252, 45, .6)'
            let [x, y] = [i * basis, j * basis];
            ctx.fillRect(x, y, basis, basis);
        }
    }

}


class Controller {
    constructor() {
        this.first_click = null;
        this.second_click = null;
    }

    async setClickOne(i, j){
        this.first_click = [i, j];
    }

    async setClickTwo(i, j){
        this.second_click = [i, j];
    }
    // REFACTOR ********************************************
    async updateGameVariables(i, j){
        let piece = await getPiece(i, j);

        if (piece && this.first_click == null){
            this.setClickOne(i, j);
        }
        else if (this.first_click != null) {
            this.setClickTwo(i, j);
            
            let [ox, oy] = this.first_click;
            let [tx, ty] = this.second_click;

            if (await canMove(ox, oy, tx ,ty)){
                this.move(ox, oy, tx, ty);
            }
            else if(piece){
                this.first_click = this.second_click = null;
                this.setClickOne(i, j);
            }
            else {
                this.first_click = this.second_click = null;
                game_variables['selected_square'] = null;
                screen.drawBoard();
            }
        }
        else{
            // console.log('do nothing');
        }
    }

    async mouseUp(e) { 
        let [ox, oy] = [moveRequest['originx'], moveRequest['originy']]
        let [i, j] = this.getMousePosition(canvasElem, e)

        if (await canMove(ox, oy, i, j)) {
            // moveRequest['targetx'] = i
            // moveRequest['targety'] = j
            this.move(ox, oy, i, j)
        }
        else if (ox != i || oy != j){
            game_variables['selected_square'] = null;
            screen.drawBoard();
        }

        $(window).off('mouseup')
        // $(window).off('mousemove')

    }
    
    async mouseDown(e) {
        let [i, j] = this.getMousePosition(canvasElem, e)
        let piece = await getPiece(i, j)

        if (piece) {
            game_variables['selected_square'] = [i, j];
            // getBoard()
            screen.drawBoard()
            moveRequest['originx'] = i
            moveRequest['originy'] = j

            $(window).on('mouseup', e => this.mouseUp(e))
            // $(window).on('mousemove', e => this.drag(e)) 
        
        }
        this.updateGameVariables(i, j).then(() => {
            // console.log(this.first_click, ' - ', this.second_click);
        })
        // piece = await getPiece(i, j);
        // console.log(i, j);
    }

    getMousePosition(canvas, event) {
        let rect = canvas.getBoundingClientRect();
        let x = event.clientX - rect.left;
        let y = event.clientY - rect.top;

        let i = Math.floor(x / basis);
        let j = Math.floor(y / basis);
        return [i, j]
    }
    
    getMouseCoord(canvas, event) {
        let rect = canvas.getBoundingClientRect();
        let x = event.clientX - rect.left;
        let y = event.clientY - rect.top;

        return [x, y]
    }
    
    async move(ox, oy, tx, ty) {
        let url = `
                /api/move?originx=${ox}&originy=${oy}&targetx=${tx}&targety=${ty}
        `
        $.getJSON(url)
        game_variables['selected_square'] = null;
        getBoard()

        this.first_click = this.second_click = null

    }

    drag(e) {
        let [x, y] = this.getMouseCoord(canvas, e);
        game_variables['mouse_position'] = [Math.floor(x), Math.floor(y)];
        // $(element).on('mousedown')
    }


}


class Piece {
    constructor(name, color, position){
        this.name = name;
        this.color = color;
        [this.i, this.j] = position;
        this.context = bg_ctx;
    }

    getSprite(){
        let sprite = `static/icons/${this.color}_${this.name}.svg`
        return sprite
    }
}



const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const bg_canvas = document.getElementById("background-canvas")
const bg_ctx = bg_canvas.getContext("2d");
const basis = 80;
const width = 90 * 8;
const height = 90 * 8;


let board_promise = fetch('/api/GET/board');
board_promise.then(res => {
    response = res;
    console.log(response);
})


let screen = new Screen();
let controller = new Controller();
let canvasElem = document.querySelector("canvas");
let moveRequest = {}


$('canvas').on('mousedown', (e) => controller.mouseDown(e))

async function getBoard() {
    board_promise = fetch('/api/GET/board');
    response = await board_promise;
    // console.log(response);
    screen.drawBoard();

    // json = $.getJSON('/api/GET/board', () => {
    //     screen.drawBoard()
    // })
}

getBoard()


function loadSprites() {
    let sprite_list = []
    let names = ['pawn', 'bishop', 'knight', 'rook', 'king', 'queen'];
    let colors = ['white', 'black'];
    names.forEach(name => {
        colors.forEach(color => {
            sprite = new Image();
            sprite.src = `static/icons/${color}_${name}.svg`
            sprite_list[`${color}_${name}`] = sprite
            // console.log(sprite.src);

        })
    })
    return sprite_list
}

let sprite_list = loadSprites()


async function canMove(ox, oy, tx, ty) {
    let canMove = false;
    let piece = await getPiece(ox, oy)

    // console.log('can move', ox, oy, tx ,ty);
    if (piece){
        piece.moves.some(move => {
            if (move.x == tx && move.y == ty) {
                canMove = true;
            }
        })
    }
    return canMove
}

async function getPiece(x, y) {
    let response = await board_promise;
    let data = await response.json();
    let piece_list = data;


    let piece_exists = false
    piece_list.some(piece => {
        if (piece.x == x && piece.y == y) {
            piece_exists = piece
            return
        }
    })
    return piece_exists
}


function resetBoard(){
    fetch('/api/reset').then(() => {
        getBoard();
    })
}

$('#reset').on('click', () => resetBoard())

// setInterval(() => {
//     screen.drawBoard()
// }, 10);

// https://www.pngwave.com/png-clip-art-dtqzc






















// XD XD XD
// Response.json: Body has already been consumed.
// Response.json: Body has already been consumed.
// Response.json: Body has already been consumed.
// Response.json: Body has already been consumed.
// Response.json: Body has already been consumed.
// Response.json: Body has already been consumed.
// Response.json: Body has already been consumed.