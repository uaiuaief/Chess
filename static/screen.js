class Screen {
    constructor() {
    }

    clearScreen() {
        ctx.clearRect(0, 0, width, height)
    }

    drawBoard() {
        this.clearScreen();
        this.highlightSquare();
        this.drawRectangle();
        this.showPossibleMoves();
        this.drawLastMovement();
        this.dragPiece();

        requestAnimationFrame(() => {
            this.drawBoard()
        })
    }

    drawBackground() {
        this.drawSquares();
        this.drawNumbers();
        this.drawLetters();
        this.drawAllPieces();

    }

    dragPiece() {
        if (controller.dragged_piece) {
            let [i, j] = controller.dragged_piece;
            let piece = board._getPiece(i, j)
            document.body.style.cursor = 'grabbing'

            if (piece && mouse.getCoord()) {
                piece.context = ctx;
                piece.draw = false;
                let [x, y] = mouse.getCoord();
                piece.context.drawImage(sprite_list[piece.sprite], x - 40, y - 40)
                piece.context = bg_ctx;
            }
        }
    }

    drawAllPieces() {
        board.pieces.map(each => {
            if (each.draw) {
                this.drawPiece(each)
            }


        })
    }

    drawPiece(piece) {
        let [i, j] = [piece.i, piece.j]

        let posX = i * basis
        let posY = j * basis
        piece.context.drawImage(sprite_list[`${piece.color}_${piece.name}`], posX + 7, posY + 4)
    }

    drawLastMovement() {
        let data = server_comm.server_info;
        if (!data || !data.last_movement) return;

        let last_movement = [data.last_movement[0], data.last_movement[1]]

        if (player_color == 'black') {
            let [ox, oy] = data.last_movement[0];
            let [tx, ty] = data.last_movement[1];
            [ox, oy] = [7 - ox, 7 - oy];
            [tx, ty] = [7 - tx, 7 - ty];
            last_movement = [[ox, oy], [tx, ty]];
        }

        if (last_movement) {
            let [originx, originy] = last_movement[0]
            let [targetx, targety] = last_movement[1]

            // ctx.fillStyle = 'rgba(140, 49, 0, .8)';
            ctx.fillStyle = 'rgba(140, 49, 0, .2)';
            let [x, y] = [originx * basis, originy * basis];
            // ctx.strokeStyle = 'rgba(140, 49, 0, .8)';
            // ctx.lineWidth = '3';
            // ctx.beginPath();
            // ctx.rect(x ,y, basis, basis);
            // ctx.stroke();
            ctx.fillRect(x, y, basis, basis);

            // ctx.fillStyle = 'rgba(248, 252, 45, .4)';
            ctx.fillStyle = 'rgba(140, 49, 0, .2)';
            [x, y] = [targetx * basis, targety * basis];
            // ctx.strokeStyle = 'white';
            // ctx.beginPath();
            // ctx.rect(x ,y, basis, basis);
            // ctx.stroke();
            ctx.fillRect(x, y, basis, basis);

        }
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
            if (player_color == 'black') {
                bg_ctx.fillText(9 - i, 2, 657 - (i * basis))
            } else {
                bg_ctx.fillText(i, 2, 657 - (i * basis))
            }

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
            if (player_color == 'black') {
                bg_ctx.fillText(letters[7 - i], (i * basis) + 64, 635)
            } else {
                bg_ctx.fillText(letters[i], (i * basis) + 64, 635)
            }
        }
    }

    drawSmallCircle(i, j) {
        let posX = (i * basis) + 40
        let posY = (j * basis) + 40
        ctx.fillStyle = 'rgba(0, 0, 0, .2)';
        ctx.beginPath();
        ctx.arc(posX, posY, 13, 0, 2 * Math.PI);
        ctx.fill()

    }

    drawCaptureSquare(i, j) {
        let posX = (i * basis) + 40
        let posY = (j * basis) + 40
        ctx.fillStyle = 'rgba(70,0,0, .2';
        ctx.strokeStyle = 'rgba(255,0,0, .9)';
        ctx.lineWidth = '1';
        ctx.beginPath();
        ctx.arc(posX, posY, 35, 0, 2 * Math.PI);
        // ctx.stroke()
        ctx.fill()
    }

    _drawCaptureSquare(i, j) {
        ctx.strokeStyle = 'rgba(254, 0, 0, .5)';
        ctx.lineWidth = '3';
        ctx.beginPath();
        ctx.rect(i * basis, j * basis, basis, basis);
        ctx.stroke();

    }

    showPossibleMoves() {
        let selected_square = controller.selected_square;
        if (selected_square) {
            let [i, j] = [selected_square[0], selected_square[1]]
            let piece = board._getPiece(i, j)
            let moves = piece.possible_moves;
            if (moves && piece.color == player_color) {
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
        let selected_square = controller.selected_square;
        if (selected_square != null) {
            let [i, j] = selected_square;
            ctx.fillStyle = 'rgba(248, 252, 45, .6)'
            let [x, y] = [i * basis, j * basis];
            ctx.fillRect(x, y, basis, basis);
        }
    }

    drawRectangle() {
        let [i, j] = mouse.getIndex();
        let piece = board._getPiece(i, j);
        if (piece) {
            ctx.strokeStyle = '#666';
            ctx.lineWidth = '3';
            ctx.beginPath();
            ctx.rect(i * basis, j * basis, basis, basis);
            ctx.stroke();
            document.body.style.cursor = 'grab';
        }
        else {
            document.body.style.cursor = 'default';
        }
    }

}

export { Screen }