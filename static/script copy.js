let game_variables = {
    'selected_square': null,
    'click_one': null,
    'click_two': null,
    'mouse_position': null,

}


const c = document.getElementById("canvas");
const ctx = c.getContext("2d");
const basis = 80;
const width = 90 * 8;
const height = 90 * 8;
let json = $.getJSON('/api/GET/board'); 
        

class Screen{
    constructor(){

    }

}

async function drawBoard() {
    ctx.clearRect(0, 0, width, height)
    drawSquares();
    highlightSquare();
    drawAllPieces();
    drawNumbers();
    drawLetters();
    showPossibleMoves();

}

function drawSquares() {
    ctx.fillStyle = '#eeeed5';
    ctx.fillRect(0, 0, width, height)
    ctx.fillStyle = '#7d945d';
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            if (i % 2 == 0) {
                if (j % 2 == 1) {
                    ctx.fillRect(j * basis, i * basis, basis, basis);
                }
            } else {
                if (j % 2 == 0) {
                    ctx.fillRect(j * basis, i * basis, basis, basis);
                }
            }
        }
    }
}

function drawNumbers() {
    for (i = 1; i <= 8; i++) {
        isPair = i % 2 == 0
        if (!isPair) {
            ctx.fillStyle = '#eeeed5'
        } else {
            ctx.fillStyle = '#7d945d'
        }
        ctx.font = 'bold 18px Arial'
        ctx.fillText(i, 3, 657 - (i * basis))
    }
}

function drawLetters() {
    letters = 'abcdefgh'
    for (i = 0; i <= 8; i++) {
        isPair = i % 2 == 0
        if (isPair) {
            ctx.fillStyle = '#eeeed5'
        } else {
            ctx.fillStyle = '#7d945d'
        }
        ctx.font = 'bold 18px Arial'
        ctx.fillText(letters[i], (i * basis) + 65, 635)
    }
}

function drawSmallCircle(i, j) {
    let posX = (i * basis) + 40
    let posY = (j * basis) + 40
    ctx.fillStyle = 'rgba(0, 0, 0, .2)';
    ctx.beginPath();
    ctx.arc(posX, posY, 10, 0, 2 * Math.PI);
    ctx.fill()

}

function drawCaptureSquare(i, j) {
    ctx.strokeStyle = 'rgba(255, 0, 0, .5)';
    ctx.lineWidth = '4';
    ctx.beginPath();
    ctx.rect(i * basis, j * basis, basis, basis);
    ctx.stroke();

}

async function showPossibleMoves() {
    let selected_square = game_variables['selected_square'];
    if (selected_square) {
        let piece = await getPiece(selected_square[0], selected_square[1])
        let moves = piece.moves;
        if (moves) {
            moves.map(async move => {
                let enemy_piece = await getPiece(move.x, move.y);
                if (enemy_piece) {
                    drawCaptureSquare(move.x, move.y)
                }
                else {
                    drawSmallCircle(move.x, move.y);
                }
            })
        }
    }
}

function highlightSquare() {
    let selected_square = game_variables['selected_square']
    if (selected_square != null) {
        [i, j] = selected_square;
        ctx.fillStyle = 'rgba(249, 252, 45, .6)'
        let [x, y] = [i * basis, j * basis];
        ctx.fillRect(x, y, basis, basis);
    }
}

async function getBoard() {
    json = $.getJSON('/api/GET/board', () => {
        drawBoard()
    })
}

getBoard()


async function drawAllPieces() {
    res = await json;
    res.map((each) => drawPiece(each))
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

let sprite_list = loadSprites()

async function drawPiece(piece) {
    let posX = piece.x * basis
    let posY = piece.y * basis
    ctx.drawImage(sprite_list[`${piece.color}_${piece.name}`], posX, posY)
}

function getMousePosition(canvas, event) {
    let rect = canvas.getBoundingClientRect();
    x = event.clientX - rect.left;
    y = event.clientY - rect.top;

    i = Math.floor(x / basis);
    j = Math.floor(y / basis);
    return [i, j]
    // console.log("column x: " + x,  
    //             "row y: " + y); 
}

let canvasElem = document.querySelector("canvas");
let moveRequest = {}


// async function updateGameVariables(i, j){
//     let piece = await getPiece(i, j);
    // console.log(piece);

    // if (piece && !game_variables['click_one']) {
    //     game_variables['click_one'] = [i, j]
    //     console.log(i, j);
    // }
    // else if (game_variables['click_one']) {
    //     let a = game_variables['click_two'] = [i, j];
    //     console.log(a);


    //     let [ox, oy] = game_variables['click_one']
    //     let [tx, ty] = game_variables['click_two']
    //     console.log(ox, oy, tx, ty);
    //     if (canMove(ox, oy, tx, ty)) {
    //         move(ox, oy, tx, ty)
    //     }
    //     game_variables['click_one'] = null;
    //     game_variables['click_two'] = null;
    // }

// }

$('canvas').on('mousedown', mouseDown)

async function mouseDown(e) {
    let [i, j] = getMousePosition(canvasElem, e)
    let piece = await getPiece(i, j)
    if (piece) {
        game_variables['selected_square'] = [i, j];
        getBoard()
        moveRequest['originx'] = i
        moveRequest['originy'] = j

        $(window).on('mouseup', mouseUp)
    }
    // updateGameVariables(i, j);
    // piece = await getPiece(i, j);
    // console.log(i, j);
}

async function mouseUp(e) {
    let [ox, oy] = [moveRequest['originx'], moveRequest['originy']]
    let [i, j] = getMousePosition(canvasElem, e)

    if (await canMove(ox, oy, i, j)) {
        moveRequest['targetx'] = i
        moveRequest['targety'] = j
        move(ox, oy, i, j)
    }
    $(window).off('mouseup')

}

function drag(element) {
    $(element).on('mousedown')
}

async function canMove(ox, oy, tx, ty) {
    let canMove = false;
    let piece = await getPiece(ox, oy)

    piece.moves.some(move => {
        if (move.x == tx && move.y == ty) {
            canMove = true;
        }
    })
    return canMove
}

async function getPiece(x, y) {
    let piece_list = await json.responseJSON;
    // console.log(piece_list);
    let piece_exists = false
    piece_list.some(piece => {
        if (piece.x == x && piece.y == y) {
            piece_exists = piece
            return
        }
    })
    // console.log(match);
    return piece_exists
}


async function move(ox, oy, tx, ty) {
    // [ox, oy] = [moveRequest['originx'], moveRequest['originy']];
    // [tx, ty] = [moveRequest['targetx'], moveRequest['targety']];
    url = `
            /api/move?originx=${ox}&originy=${oy}&targetx=${tx}&targety=${ty}
    `
    $.getJSON(url)
    game_variables['selected_square'] = null;
    getBoard()

}

// setInterval(drawBoard, 100)
// requestAnimationFrame(drawBoard)
// canvasElem.addEventListener("mousemove", function(e) 
// { 
//     getMousePosition(canvasElem, e); 
// }); 


// $('canvas').on('drag', (e) => {
//         console.log('a');
// })