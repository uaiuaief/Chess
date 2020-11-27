class HUD {
    constructor() {
        this.current_screen = null;
        this.countdown_active = false;

        $('#reset').on('click', () => {
            this.resetBoard()
            this.changeToScreen('start-screen');
        })

        $('.restart').on('click', () => hud.rematch())

        $('.play-button').on('click', () => {
            this.changeToScreen('choose-game-type');
        })

        $('.against-human').on('click', () => {
            this.changeToScreen('connection-status');
        })
        $('.against-computer').on('click', () => {
            this.changeToScreen();
            fetch(`/api/play?minutes=60`)
        })

        $('.time').on('click', (e) => {
            this.changeToScreen('count-down');
            let minutes = e.target.name;
            hud.chooseTime(minutes)
        })
    }

    changeToScreen(screen){
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
            if (sc != screen){
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

        console.log(this.current_screen);
        let connections = data.players.filter(player => {
            if (player.connected) return true;
        })

        if (connections.length == 1) {
            $('.player-one-connection').addClass("connected");
            $('.player-two-connection').removeClass("connected");

            if (data.game_started == false) {
                // $('.screen-wrapper').show();
                // $('.screen-cover').show();
            }
        }
        else if (connections.length == 2) {
            $('.player-one-connection').addClass("connected");
            $('.player-two-connection').addClass("connected");

            if (this.current_screen == 'connection-status' && data.game_started == false) {
                setTimeout(() => {
                    this.changeToScreen('choose-time');
                }, 1000);
            }

        }
        else {
            $('.player-one-connection').removeClass("connected");
            $('.player-two-connection').removeClass("connected");
        }
    }

    rematch() {
        this.resetBoard();
        this.changeToScreen();
        audio.game_start.play()
        server_comm.time_up_handled = false;
        server_comm.tenseconds_warning_played = false;
        mouse.activateControllers();
    }

    chooseTime(minutes) {
        this.startGame(minutes);
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
        this.countdown_active = true;
        this.countDown(3, (seconds) => {
            console.log(seconds);
            let text = `Game starting in ${seconds}`
            $('.count-down').text(text);
        });


        // for (let i = 3; i > 0; ){
        //     setTimeout(() => {
        //         console.log(i);
        //         i--;
        //         // let text = `Game starting in ${i}`
        //         // $('.connection-status').text(text);
        //     }, 1000);
        // }
        // $('.start-screen').hide();
        // $('.connection-status').hide();
        // $('.choose-time').show();

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

    decreaseClockTime(data) {
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