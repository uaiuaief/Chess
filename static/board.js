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
        })
        this.pieces = new_array;
    }

    _getPiece(i, j) {
        let piece = this.pieces.filter(each => {
            return (each.i == i && each.j == j)
        })
        if (piece[0]) {
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

    invert() {
        this.pieces.forEach(piece => {
            piece.i = 7 - piece.i
            piece.j = 7 - piece.j

            piece.possible_moves.forEach(move => {
                move.x = 7 - move.x;
                move.y = 7 - move.y;
            })
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

export { Board }