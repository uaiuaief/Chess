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
        // this.drawBackground();
    }

    async getPieces() {
        let piece_list = [];
        let res = await board_state;
        let clone = res.clone();
        let data = await clone.json();

        data.map(each => {
            piece_list.push(new Piece(each.name, each.color, [each.x, each.y]))
        })

        return piece_list;
    }

    async findPiece(i, j) {
        let piece_list = await this.getPieces();
        let piece = null;
        piece_list.some(each => {
            let same_row = (each.i == i);
            let same_column = (each.j == j);

            if (same_row && same_column) {
                piece = each;
                return
            }
        })
        return piece;
    }

    clearScreen() {
        ctx.clearRect(0, 0, width, height)
    }

    drawBoard() {
        this.clearScreen();
        this.highlightSquare();
        // this.drawAllPieces();
        this.showPossibleMoves();

        this._dragPiece();

        requestAnimationFrame(async () => {
            screen.drawBoard()
        })
    }

    drawBackground() {
        this.drawSquares();
        this.drawNumbers();
        this.drawLetters();
        this._drawAllPieces();
    }

    async drawAllPieces() {
        let res = await board_state;
        let clone = res.clone();
        let data = await clone.json();

        data.map((each) => this.drawPiece(each))
    }

    async drawPiece(piece) {
        let posX = piece.x * basis
        let posY = piece.y * basis
        ctx.drawImage(sprite_list[`${piece.color}_${piece.name}`], posX, posY)

    }

    // TODO
    _dragPiece() {
        if (game_variables['dragged_piece']) {
            let [i, j] = game_variables['dragged_piece'];
            let piece = board._getPiece(i, j)

            if (piece && game_variables['mouse_position']) {
                piece.context = ctx;
                // piece.draw = false;
                let [x, y] = game_variables['mouse_position'];
                piece.context.drawImage(sprite_list[piece.sprite], x - 40, y - 40)
                piece.context = bg_ctx;
            }
        }
    }

    async _drawAllPieces() {
        // await board.loadPieces()
        board.pieces.map(each => {
            if (each.draw) {
                // console.log(each);
                this._drawPiece(each)
            }


        })
    }

    _drawPiece(piece) {
        let posX = piece.i * basis
        let posY = piece.j * basis
        piece.context.drawImage(sprite_list[`${piece.color}_${piece.name}`], posX, posY)
    }



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

    showPossibleMoves() {
        let selected_square = game_variables['selected_square'];
        if (selected_square) {
            let [i, j] = [selected_square[0], selected_square[1]]
            let piece = board._getPiece(i, j)
            let moves = piece.possible_moves;
            if (moves) {
                moves.map(move => {
                    let enemy_piece = board._getPiece(move.x, move.y);
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

    async setClickOne(i, j) {
        this.first_click = [i, j];
    }

    async setClickTwo(i, j) {
        this.second_click = [i, j];
    }
    // REFACTOR ********************************************
    async updateGameVariables(i, j) {
        let piece = await getPiece(i, j);

        if (piece && this.first_click == null) {
            this.setClickOne(i, j);
        }
        else if (this.first_click != null) {
            this.setClickTwo(i, j);

            let [ox, oy] = this.first_click;
            let [tx, ty] = this.second_click;

            if (await canMove(ox, oy, tx, ty)) {
                this.move(ox, oy, tx, ty);
            }
            else if (piece) {
                this.first_click = this.second_click = null;
                this.setClickOne(i, j);
            }
            else {
                this.first_click = this.second_click = null;
                game_variables['selected_square'] = null;
                screen.drawBoard();
            }
        }
        else {
            // console.log('do nothing');
        }
    }

    async mouseUp(e) {
        let [ox, oy] = [moveRequest['originx'], moveRequest['originy']]
        let [i, j] = this.getMousePosition(canvasElem, e)

        if (await canMove(ox, oy, i, j)) {
            this.move(ox, oy, i, j)
        }
        else if (ox != i || oy != j) {
            game_variables['selected_square'] = null;
            board.drawAllTrue();
            screen.drawBackground();
        }
        else{
            board.drawAllTrue();
            screen.drawBackground();
        }


        game_variables['dragged_piece'] = null;
        // game_variables['selected_square'] = null;
        $(window).off('mouseup')
        $(window).off('mousemove')

    }

    async mouseDown(e) {
        let [i, j] = this.getMousePosition(canvasElem, e)
        let [x, y] = this.getMouseCoord(canvasElem, e)
        let piece = await getPiece(i, j)
        game_variables['mouse_position'] = [Math.floor(x), Math.floor(y)];

        if (piece) {
            game_variables['selected_square'] = [i, j];
            game_variables['dragged_piece'] = [i, j];

            moveRequest['originx'] = i
            moveRequest['originy'] = j


            let selected_piece = board._getPiece(i, j)
            selected_piece.draw = false;
            // console.log(testpiece);
            screen.drawBackground();


            $(window).on('mouseup', e => this.mouseUp(e))
            $(window).on('mousemove', e => this.drag(e))


        }
        // screen.drawBackground();
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
        game_variables['dragged_piece'] = null;
        getBoard()

        this.first_click = this.second_click = null

    }

    drag(e) {
        let [x, y] = this.getMouseCoord(canvas, e);
        let [i, j] = this.getMousePosition(canvas, e);
        game_variables['mouse_position'] = [Math.floor(x), Math.floor(y)];
    }


}

class Board {
    constructor() {
        this.pieces = [];
    }

    async loadPieces() {
        let new_array = [];
        let res = await board_state;
        let clone = res.clone()
        let data = await clone.json();

        data.map(each => {
            new_array.push(new Piece(each.name, each.color, [each.x, each.y], each.moves))
            // console.log(each);
        })
        this.pieces = new_array;
    }

    _getPiece(i, j) {
        let piece = this.pieces.filter(each => {
            return (each.i == i && each.j == j)
        })
        if (piece) {
            return piece[0]
        }
        else {
            return false
        }
    }

    drawAllTrue(){
        this.pieces.forEach(piece => {
            piece.draw = true;
        })
    }
}

class Piece {
    constructor(name, color, position, moves) {
        this.draw = true;
        this.drag = false;
        this.name = name;
        this.color = color;
        [this.i, this.j] = position;
        this.context = bg_ctx;
        this.sprite = `${color}_${name}`;
        this.possible_moves = moves;
    }
}



const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const bg_canvas = document.getElementById("background-canvas")
const bg_ctx = bg_canvas.getContext("2d");
const basis = 80;
const width = 90 * 8;
const height = 90 * 8;

async function loadEverything() {

    board_state = fetch('/api/GET/board')
    board = new Board();
    screen = new Screen();
    controller = new Controller();
    canvasElem = document.querySelector("canvas");
    moveRequest = {}

    sprite_list = loadSprites()

}

loadEverything().then(() => getBoard())



// console.log(board.pieces);


let test_sp = new Image()
test_sp.src = '/static/icons/black_pawn.svg'





$('canvas').on('mousedown', (e) => controller.mouseDown(e))

async function getBoard() {
    board_state = await fetch('/api/GET/board');
    await board.loadPieces();
    // screen.drawBoard();
    screen.drawBackground();


    // bg_ctx.fillStyle = 'black'
    // bg_ctx.fillRect(200,200,50,50)
}


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



async function canMove(ox, oy, tx, ty) {
    let canMove = false;
    let piece = await getPiece(ox, oy)

    // console.log('can move', ox, oy, tx ,ty);
    if (piece) {
        piece.moves.some(move => {
            if (move.x == tx && move.y == ty) {
                canMove = true;
            }
        })
    }
    return canMove
}

async function getPiece(x, y) {
    let res = await board_state;
    let clone = res.clone()
    let data = await clone.json();
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


function resetBoard() {
    fetch('/api/reset').then(() => {
        getBoard();
    })
}

$('#reset').on('click', () => resetBoard())


// setInterval(() => {
requestAnimationFrame(() => {
    console.log('first');
    screen.drawBoard()
})
// }, 16);

// https://www.pngwave.com/png-clip-art-dtqzc




