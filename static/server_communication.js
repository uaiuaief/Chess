class ServerCommunication {
    time_up_handled = false;
    tenseconds_warning_played = false;

    handleTimeUp(data) {
        if (!this.time_up_handled) {
            hud.showTimeUpScreen(data);
            this.time_up_handled = true;
        }
    }

    handleTurnChange(data) {
        hud.changeClockTurn();
        turn_count = data.turn_count;
        this.getBoard();

        if (data.check_mate) {
            hud.showCheckMateScreen(data);
        }
    }

    handleTimer(data) {
        hud.decreaseClockTime(data);
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
                        if (turn == player_color) {
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
                            [ox, oy] = [7 - ox, 7 - oy];
                            [tx, ty] = [7 - tx, 7 - ty];
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

    async getBoard() {
        board_state = await fetch('/api/GET/board');
        await board.loadPieces();
        if (player_color == 'black') {
            board.invert()
        }
        screen.drawBackground();
    }
}

export { ServerCommunication }