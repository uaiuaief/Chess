
class Controller {
    constructor() {
        this.first_click = null;
        this.second_click = null;

        this.selected_square = null;
        this.dragged_piece = null;

        this.origin_square = null;
        this.target_square = null;
    }

    invertIfBlack(i, j) {
        if (player_color == 'black') {
            return [7 - i, 7 - j]
        }
        else {
            return [i, j]
        }
    }

    setClickOne(i, j) {
        this.first_click = [i, j];
    }

    setClickTwo(i, j) {
        this.second_click = [i, j];
    }

    async updateGameVariables(i, j) {
        let piece = board._getPiece(i, j);

        if (piece && this.first_click == null) {
            this.setClickOne(i, j);
        }
        else if (this.first_click) {
            this.setClickTwo(i, j);

            let [ox, oy] = this.first_click;
            let [tx, ty] = this.second_click;
            let origin_piece = board._getPiece(ox, oy);
            if (canMove(origin_piece, tx, ty)) {
                this.move(ox, oy, tx, ty);
            }
            else if (piece) {
                this.first_click = this.second_click = null;
                this.setClickOne(i, j);
            }
            else {
                this.first_click = this.second_click = null;
                this.selected_square = null;
            }
        }

    }

    async mouseUp(e) {
        let [ox, oy] = this.origin_square;
        let [i, j] = mouse.getIndex();
        let piece = board._getPiece(ox, oy)

        if (canMove(piece, i, j)) {
            this.move(ox, oy, i, j)
        }
        else if (ox != i || oy != j) {
            this.selected_square = null;
            this.first_click = this.second_click = null;
            board.drawAllTrue();
            screen.drawBackground();
            audio.illegal.play()
        }
        else {
            board.drawAllTrue();
            screen.drawBackground();
        }


        this.dragged_piece = null;
        $(window).off('mouseup')


    }

    async mouseDown(e) {
        $(`.white`).hide();
        $(`.black`).hide();

        let [i, j] = mouse.getIndex()
        let piece = board._getPiece(i, j);

        if (piece) {
            this.selected_square = [i, j];
            this.dragged_piece = [i, j];

            this.origin_square = [i, j]


            let selected_piece = board._getPiece(i, j)
            selected_piece.draw = false;
            screen.drawBackground();


            $(window).on('mouseup', e => this.mouseUp(e))
        }
        this.updateGameVariables(i, j).then(() => {
        })
    }

    async move(ox, oy, tx, ty, skip_promotion = false) {
        // if (turn != player_color) {
        //     this.selected_square = null;
        //     this.dragged_piece = null; 
        //     server_comm.getBoard()
        //     this.first_click = this.second_click = null
        //     return
        // }

        if (!skip_promotion) {
            [ox, oy] = this.invertIfBlack(ox, oy);
            [tx, ty] = this.invertIfBlack(tx, ty);
        }


        let piece;
        let enemy_piece;
        if (player_color == 'black') {
            piece = board._getPiece(7 - ox, 7 - oy)
            enemy_piece = board._getPiece(7 - tx, 7 - ty);
        } else {
            piece = board._getPiece(ox, oy)
            enemy_piece = board._getPiece(tx, ty);
        }


        // if (turn != piece.color) {
        //     this.selected_square = null;
        //     this.dragged_piece = null; 
        //     server_comm.getBoard()
        //     this.first_click = this.second_click = null
        //     return
        // }

        if (!skip_promotion && piece.name == 'pawn' && (ty == 0 || ty == 7)) {
            this.showPromotions(piece.color, ox, oy, () => this.move(ox, oy, tx, ty, true))
        } else {
            let move_url = `
                    /api/move?originx=${ox}&originy=${oy}&targetx=${tx}&targety=${ty}
            `
            fetch(move_url)
            this.selected_square = null;
            this.dragged_piece = null;
            server_comm.getBoard()
            this.first_click = this.second_click = null

            fetch('/api/changes').then(res => res.json()
                .then(data => {
                    if (!data.game_started){
                        audio.illegal.play()
                    }
                    else if (data.check) {
                        audio.move_check.play();
                    }
                    else if (skip_promotion) {
                        audio.promote.play();
                    }
                    else if (piece.name == 'king' && Math.abs(ox-tx) == 2) {
                        audio.castle.play();
                    }
                    else if (enemy_piece) {
                        audio.capture.play();
                    }
                    else {
                        audio.move_self.play();
                    }
                })
            )
        }
    }

    showPromotions(color, ox, oy, callback) {
        this.selected_square = null;
        this.dragged_piece = null;
        server_comm.getBoard()
        this.first_click = this.second_click = null
        $(`.${color}`).show();
        if (color == 'black') {
            $(`.${color}`).css({ "left": `${(7 - ox) * 80}px` })
        } else {
            $(`.${color}`).css({ "left": `${ox * 80}px` })
        }

        $('.promotion').on('click', async event => {
            let promotion = event.target.name;
            await fetch(`/api/promote?x=${ox}&y=${oy}&promotion=${promotion}`)
            callback()
            $(`.${color}`).hide()
            $('.promotion').off("click")
        })


    }

}

function canMove(piece, tx, ty) {
    let canMove = false;
    if (piece) {
        piece.possible_moves.some(move => {
            if (move.x == tx && move.y == ty) {
                canMove = true;
            }
        })
    }
    return canMove
}


export { Controller }