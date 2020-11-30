class HUD {
    constructor() {
        this.current_screen = null;
        this.countdown_active = false;
        this.timer = null;

        $('#reset').on('click', () => {
            this.resetBoard()
            this.changeToScreen('start-screen');
            this.timer = null;
            $('.timer').text('-- : --')

        })

        $('.restart').on('click', () => hud.rematch())

        $('.play-button').on('click', () => {
            this.changeToScreen('choose-game-type');
        })

        $('.against-human').on('click', () => {
            this.changeToScreen('choose-time');
        })
        $('.against-computer').on('click', () => {
            this.changeToScreen();
            fetch(`/api/computer`)
        })

        $('.time').on('click', (e) => {
            this.current_screen = null;
            this.changeToScreen('waiting-opponent');
            $('.screen-wrapper').hide();
            let minutes = e.target.name;
            hud.chooseTime(minutes)
        })
    }

    changeToScreen(screen) {
        if (!screen) {
            $('.screen-wrapper').hide();
            $('.screen-cover').hide();
            this.current_screen = null;
            return
        }

        this.current_screen = screen;
        let screen_list = [
            'start-screen',
            'choose-game-type',
            'connection-status',
            'choose-time',
            'count-down',
            'check-mate'
        ];

        $('.screen-wrapper').show();
        $('.screen-cover').show();
        $(`.${screen}`).show();
        screen_list.forEach(sc => {
            if (sc != screen) {
                $(`.${sc}`).hide();
            }
        })

    }

    resetBoard() {
        // console.log(server_comm.server_info);
        fetch('/api/reset').then(() => {
            server_comm.getBoard();
        })
    }

    showStartScreen() {
        if (player_color == 'black') return;
        this.changeToScreen('start-screen');
        $('.screen-cover').show();
    }

    handlePlayerConnection() {
        let data = server_comm.server_info
        if (!data) return;

        // console.log(this.current_screen);
        let connections = data.players.filter(player => {
            if (player.connected) return true;
        })

        if (connections.length == 1) {
            $('.player-one-connection .connection-icon').addClass("connected");
            $('.player-two-connection .connection-icon').removeClass("connected");

            if (data.game_started == false) {
                // $('.screen-wrapper').show();
                $('.screen-cover').show();
            }
        }
        else if (connections.length == 2) {
            $('.player-one-connection .connection-icon').addClass("connected");
            $('.player-two-connection .connection-icon').addClass("connected");

            if (this.timer && !data.game_started && this.current_screen != 'choose-time') {
                this.startGame(this.timer);
            }
        }
        else {
            $('.player-one-connection .connection-icon').removeClass("connected");
            $('.player-two-connection .connection-icon').removeClass("connected");
        }
    }

    rematch() {
        this.resetBoard();

        if (server_comm.server_info.against_computer) {
            this.changeToScreen('start-screen');
        }
        else {
            this.timer == null;
            this.changeToScreen('choose-time');
            // console.log(this.timer);
            // this.startGame();
            audio.game_start.play()
        }
        server_comm.time_up_handled = false;
        server_comm.tenseconds_warning_played = false;
        server_comm.detectChanges();
        mouse.activateControllers();

    }

    chooseTime(minutes) {
        $('.timer').text(`${minutes}:00`)
        // this.startGame(minutes);
        this.timer = minutes;
    }

    countDown(seconds, callback) {
        setTimeout(() => {
            callback(seconds)
            seconds--;
            if (seconds >= 0) {
                this.countDown(seconds, (seconds) => callback(seconds));
            }
            else {
                this.changeToScreen()
                $('.count-down').text('Game starting in 3')
            }
        }, 1000);
    }

    startGame(minutes) {
        fetch(`/api/play?minutes=${minutes}`)
        // mouse.activateControllers();
        this.changeToScreen('');
        audio.game_start.play();

    }

    showCheckMateScreen(data) {
        $('.end-game-text').text('Check Mate')
        $('.winner').text(`${data.winner} wins`)
        this.changeToScreen('check-mate');
        audio.game_end.play();
        // mouse.deactivateControllers();
        document.body.style.cursor = 'default';
    }

    showTimeUpScreen(data) {
        $('.end-game-text').text(`Time's up`)
        $('.winner').text(`${data.time_up} wins`)
        this.changeToScreen('check-mate');
        audio.game_end.play();
    }

    changeClockTurn() {
        if (turn == player_color) {
            $('.self-timer').addClass("active")
            $('.enemy-timer').removeClass("active")
        }
        else {
            $('.enemy-timer').addClass("active")
            $('.self-timer').removeClass("active")
        }

    }

    getChessCode(color, name) {
        let chess_code;
        color = 'white';
        switch (name) {
            case 'pawn':
                chess_code = (color == 'white') ? '&#9823;' : '&#9817;';
                break;
            case 'knight':
                chess_code = (color == 'white') ? '&#9822;' : '&#9816;';
                break;
            case 'bishop':
                chess_code = (color == 'white') ? '&#9821;' : '&#9815;';
                break;
            case 'rook':
                chess_code = (color == 'white') ? '&#9820;' : '&#9814;';
                break;
            case 'queen':
                chess_code = (color == 'white') ? '&#9819;' : '&#9813;';
                break;
            case 'king':
                chess_code = (color == 'white') ? '&#9818;' : '&#9812;';
                break;
        }
        return chess_code

    }

    addToCapturedPieces(color, name) {
        let player = (player_color == color) ? 'self' : 'enemy';

        let chess_code = this.getChessCode(color, name)
        if (color == player_color) {
            if (name == 'pawn') {
                $('.captured-pieces.enemy .pawn').prepend(chess_code);
            }
            else {
                $('.captured-pieces.enemy .others').append(chess_code);
            }
        }
        else {
            if (name == 'pawn') {
                $('.captured-pieces.self .pawn').prepend(chess_code);
            }
            else {
                $('.captured-pieces.self .others').append(chess_code);
            }
        }
    }

    updateCapturedPieces() {
        $('.others').text('');
        $('.pawn').text('');

        const compare_function = (a, b) => {
            let get_value = (name) => {
                if (name == 'pawn') return 0;
                else if (name == 'bishop') return 1;
                else if (name == 'knight') return 2;
                else if (name == 'rook') return 3;
                else if (name == 'queen') return 4;
            }
            a = get_value(a);
            b = get_value(b);
            return (a - b);
        }

        let captured_white =
            server_comm.server_info.captured_pieces.
                filter(piece => piece.color == 'white').
                map(piece => piece.name).
                sort(compare_function);

        let captured_black =
            server_comm.server_info.captured_pieces.
                filter(piece => piece.color == 'black').
                map(piece => piece.name).
                sort(compare_function);

        captured_white.forEach(name => this.addToCapturedPieces('white', name));
        captured_black.forEach(name => this.addToCapturedPieces('black', name));
        // console.log(name);
        //     let chess_code = this.getChessCode('black', name)
        //     if (player_color == 'white') {
        //         if (name == 'pawn') {
        //             $('.captured-pieces.self .pawn').prepend(chess_code);
        //         }
        //         else {
        //             $('.captured-pieces.self .others').append(chess_code);
        //         }
        //     }
        //     else {
        //         if (name == 'pawn') {
        //             $('.captured-pieces.enemy .pawn').prepend(chess_code);
        //         }
        //         else {
        //             $('.captured-pieces.enemy .others').append(chess_code);
        //         }
        //     }
        // })
        // console.log(captured_white);

        // server_comm.server_info.captured_pieces.forEach(piece => {
        //     this.addToCapturedPieces(piece.color, piece.name)
        // let chess_code = this.getChessCode(piece.color, piece.name)
        // if (piece.color == player_color) {
        //     if (piece.name == 'pawn') {
        //         $('.captured-pieces.enemy .pawn').prepend(chess_code);
        //     }
        //     else {
        //         $('.captured-pieces.enemy .others').append(chess_code);
        //     }
        // }
        // else {
        //     if (piece.name == 'pawn') {
        //         $('.captured-pieces.self .pawn').prepend(chess_code);
        //     }
        //     else {
        //         $('.captured-pieces.self .others').append(chess_code);
        //     }
        // }
        // })
    }

    decreaseClockTime(data) {
        if (!data.game_started) return;

        let player_date = new Date(0);
        player_date.setSeconds(data.timer[player_color]);
        var player_timer = player_date.toISOString().substr(14, 5);

        let enemy_date = new Date(0);
        enemy_date.setSeconds(data.timer[enemy_color]);
        var enemy_timer = enemy_date.toISOString().substr(14, 5);

        $('.self-timer').text(player_timer)
        $('.enemy-timer').text(enemy_timer)

    }
}


export { HUD }