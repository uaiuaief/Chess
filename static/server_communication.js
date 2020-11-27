class ServerCommunication {
    constructor() {
        this.time_up_handled = false;
        this.tenseconds_warning_played = false;
        this.server_info = null;

        window.loop.addFunction(() => {
            this.handleTimeUp(this.server_info);
            this.handleTimer(this.server_info);
            this.handlePlayerMove(this.server_info);
            hud.handlePlayerConnection();
        })
    }

    handlePlayerMove(data) {
        if (!data) return;
        if (move_count != data.move_count) {
            this.handleTurnChange(data);
            this.updateBoardHistory(data);
            this.handleMovementAudio(data);
        }
    }

    handleMovementAudio(data) {
        if (turn == player_color) {
            if (data.last_movement_castle) {
                audio.castle.play();
            }
            else if (data.check) {
                audio.move_check.play();
            }
            else if (data.last_movement_capture) {
                audio.capture.play();
            }
            else {
                audio.move_opponent.play();
            }
        }
    }

    updateBoardHistory(data) {
        $('.white-turn').text('')
        $('.black-turn').text('')
        $('.turn-count').text('')
        for (let key in data.move_history) {
            let move = data.move_history[key]
            let white_move = move['white'];
            let black_move = move['black'] ? move['black'] : ' ';
            $('.turn-count').append(`<div class="turn-count-number line">${key}.</div>`);
            $('.white-turn').append(`<p class="line white-move">${white_move}</p>`);
            $('.black-turn').append(`<div class="line black-move">${black_move}</div>`);
        }
    }

    handleTimeUp(data) {
        if (!data) return;
        if (data.time_up && !this.time_up_handled) {
            hud.showTimeUpScreen(data);
            this.time_up_handled = true;
        }
    }

    handleTurnChange(data) {
        hud.changeClockTurn();
        turn_count = data.turn_count;
        move_count = data.move_count;
        this.getBoard();

        if (data.check_mate) {
            hud.showCheckMateScreen(data);
        }
    }

    handleTimer(data) {
        if (!data) return;
        hud.decreaseClockTime(data);
        turn = data.current_turn;

        if (data.game_started && !this.tenseconds_warning_played && data.timer[player_color] <= 11) {
            audio.tenseconds.play()
            this.tenseconds_warning_played = true;
        }
    }

    detectChanges() {
        fetch(`/api/changes`).then((res) => res.json()
            .then(data => {
                this.server_info = data;

                
            })
        )
    }

    async getBoard() {
        board_state = await fetch('/api/GET/board');
        await board.loadPieces();
        if (player_color == 'black') {
            board.invert()
        }
        screen.drawBackground();
        let element = document.querySelector('.move-history');
        element.scrollTo(0, element.scrollHeight)
    }
}

export { ServerCommunication }