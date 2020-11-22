class Mouse {
    constructor() {
        this.x
        this.y
        // $(window).on('mousemove', (e) => this.move(e))
        // $('canvas').on('mousedown', (e) => this.b1_down(e))
    }

    activateControllers() {
        $(window).on('mousemove', (e) => this.move(e))
        $('canvas').on('mousedown', (e) => this.b1_down(e))
    }

    deactivateControllers() {
        $(window).off('mousemove')
        $('canvas').off('mousedown')
    }

    getCoord() {
        return [this.x, this.y]
    }

    setCoord(x, y) {
        this.x = x;
        this.y = y;
    }

    getIndex() {
        let i = Math.floor(this.x / 80);
        let j = Math.floor(this.y / 80);

        return [i, j]
    }

    move(event) {
        let rect = canvas.getBoundingClientRect();
        let x = event.clientX - rect.left;
        let y = event.clientY - rect.top;

        this.setCoord(x, y)
    }

    b1_down(event) {
        if (event.originalEvent.button == 0) {
            window.controller.mouseDown(event)
        }
    }
}

export { Mouse }