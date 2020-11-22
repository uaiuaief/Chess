class AudioPlayer {
    capture = new Audio('/static/audio/capture.wav')
    move_self = new Audio('/static/audio/move-self.wav')
    move_opponent = new Audio('/static/audio/move-opponent.wav')
    illegal = new Audio('/static/audio/illegal.wav')
    game_end = new Audio('/static/audio/game-end.wav')
    game_start = new Audio('/static/audio/game-start.wav')
    move_check = new Audio('/static/audio/move-check.wav')
    promote = new Audio('/static/audio/promote.wav')
    tenseconds = new Audio('/static/audio/tenseconds.wav')
    premove = new Audio('/static/audio/premove.wav')
    castle = new Audio('/static/audio/castle.wav')
}

export {AudioPlayer}