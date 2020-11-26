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
        move_count = data.move_count;
        this.getBoard();

        if (data.check_mate) {
            hud.showCheckMateScreen(data);
        }
    }

    handleTimer(data) {
        hud.decreaseClockTime(data);
        turn = data.current_turn;

        if (!this.tenseconds_warning_played && data.timer[player_color] <= 11) {
            audio.tenseconds.play()
            this.tenseconds_warning_played = true;
        }
    }

    detectChanges() {
        fetch(`/api/changes`)
            .then((res) => res.json()
                .then(data => {
                    // $('.test').empty();
                    // if (data.game_over && player_color == 'white') {
                    //     $('.start-screen-wrapper').show();
                    // }
                    let connections = data.players.filter(player => {
                        if (player.connected) return true;
                    })
                    console.log(connections[1]);

                    if (connections.length == 1) {
                        $('.player-one-connection').addClass("connected");
                        $('.player-two-connection').removeClass("connected");
                    } 
                    else if (connections.length == 2) {
                        $('.player-one-connection').addClass("connected");
                        $('.player-two-connection').addClass("connected");
                    }
                    else {
                        $('.player-one-connection').removeClass("connected");
                        $('.player-two-connection').removeClass("connected");
                    }
                        // console.log(player_color);
                        if (data.game_over){
                            // for (let i = 3; i >= 0; i--){
                            //     console.log(i);
                            //     let text = `Game starting in ${i}`
                            //     $('.connection-status').text(text);
                            //     // setTimeout(() => {},1000);
                            // }
                            // $('.start-screen').hide();
                            // $('.connection-status').hide();
                            // $('.choose-time').show();
                        }
                    

                    // console.log(data.players);
                    this.handleTimer(data);

                    if (move_count != data.move_count) {
                        this.handleTurnChange(data);
                        if (turn == player_color) {
                            if (data.last_movement_castle) {
                                audio.castle.play();
                            }
                            else if (data.last_movement_capture) {
                                audio.move_check.play();
                            }
                            else {
                                audio.move_opponent.play();
                            }
                        }


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
        let element = document.querySelector('.move-history');
        element.scrollTo(0, element.scrollHeight)
    }
}

export { ServerCommunication }