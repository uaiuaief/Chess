class HUD {
    constructor() {
        $('#reset').on('click', () => {
            this.resetBoard()
            hud.showStartScreen();
        })

        $('.restart').on('click', () => hud.rematch())

        $('.play-button').on('click', () => {
            $('.start-screen').hide();
            $('.choose-game-type').show();
        })

        $('.against-human').on('click', () => {
            $('.choose-game-type').hide();
            $('.connection-status').show();
            // $('.choose-time').show();
        })
        $('.against-computer').on('click', () => {
            $('.choose-game-type').hide();
            $('.start-screen-wrapper').hide();
            hud.chooseTime(60)
        })

        $('.time').on('click', (e) => {
            $('.choose-time').hide();
            // $('.connection-status').show();
            let minutes = e.target.name;
            hud.chooseTime(minutes)
        })
    }

    resetBoard() {
        fetch('/api/reset').then(() => {
            server_comm.getBoard();
        })
    }

    showStartScreen() {
        if (player_color == 'black') return;

        $('.choose-time').hide();
        $('.choose-game-type').hide();
        $('.connection-status').hide();

        $('.start-screen-wrapper').show();
        $('.start-screen').show();
        // $('.start-2').hide();
        $('.screen-cover').show();
    }

    rematch() {
        this.resetBoard()
        $('#check-mate').hide();
        $('.screen-cover').hide();
        audio.game_start.play()
        server_comm.time_up_handled = false;
        server_comm.tenseconds_warning_played = false;
        mouse.activateControllers();
    }

    chooseTime(minutes) {
        $('.start-screen-wrapper').hide();
        $('.choose-time').hide();
        $('.screen-cover').hide();
        this.startGame(minutes);
    }

    startGame(minutes) {
        fetch(`/api/play?minutes=${minutes}`)
        // mouse.activateControllers();
        audio.game_start.play();

    }

    showCheckMateScreen(data) {
        $('.end-game-text').text('Check Mate')
        $('.winner').text(`${data.winner} wins`)
        $('#check-mate').show();
        $('.screen-cover').show();
        audio.game_end.play();
        // mouse.deactivateControllers();
        document.body.style.cursor = 'default';
    }

    showTimeUpScreen(data) {
        $('.end-game-text').text(`Time's up`)
        $('.winner').text(`${data.time_up} wins`)
        $('#check-mate').show();
        $('.screen-cover').show();
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