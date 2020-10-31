from tkinter import *
from main import *


class Controller:
    def __init__(self):
        self.origin = None
        self.target = None

    def send(self):
        if self.origin and self.target:
            board.move(self.origin, self.target)
            self.origin = None
            self.target = None


class ViewPiece:
    def __init__(self, piece, i, j):
        self.PIECE = piece
        self.NAME = self.PIECE.NAME
        self.COLOR = self.PIECE.COLOR
        self.i = i
        self.j = j
        # self.x, self.y = self.get_coord()
        self.x = (self.i * 100) + 50
        self.y = (self.j * 100) + 50

    def get_coord(self):
        # sqr_x = (self.i * 100) + 50
        # sqr_y = (self.j * 100) + 50

        # return sqr_x, sqr_y
        return self.x, self.y

    def set_coord(self, x, y):
        self.x = x
        self.y = y

    def get_index(self):
        return self.i, self.j

    def set_index(self, i, j):
        self.i = i
        self.j = j


class ViewBoard:
    def __init__(self):
        self.pieces = []
        self.selected_piece = None

    def get_piece(self, i, j):
        for each in self.pieces:
            if each.get_index() == (i, j):
                return each


C = Controller()
root = Tk()
canvas = Canvas(root, width=800, height=800, background='gray')
canvas.pack()

board = Board()
grid = board.GRID
v_board = ViewBoard()


def setup_view_board():
    for row in grid:
        for cell in row:
            piece = cell.get_piece()
            if piece:
                i, j = cell.POSITION

                v_piece = ViewPiece(piece, i, j)
                v_board.pieces.append(v_piece)

setup_view_board()
def draw_board():
    for piece in v_board.pieces:
            x, y = piece.get_coord()
            canvas.create_text(x, y, anchor="center", text=piece.NAME, fill=piece.COLOR, font='helvetica 15')


def draw_grid():
    for i in range(7):
        canvas.create_line((i+1)*100, 0, (i+1)*100, 800, fill='#333')
        canvas.create_line(0, (i+1)*100, 800, (i+1)*100, fill='#333')


def pixel_to_square(x, y):
    sqr_x = (x // 100) * 100 + 50
    sqr_y = (y // 100) * 100 + 50

    return sqr_x, sqr_y


def index_to_square(i, j):
    sqr_x = (i * 100) + 50
    sqr_y = (j * 100) + 50

    return sqr_x, sqr_y


def pixel_to_index(x, y):
    i = x//100
    j = y//100

    return i, j


def drag(event):
    if v_board.selected_piece:
        x, y = event.x, event.y
        # print(x, y)
        v_board.selected_piece.set_coord(x, y)
        print(v_board.selected_piece.get_coord())


def click(event):
    x, y = event.x, event.y
    i, j = pixel_to_index(x, y)

    v_board.selected_piece = v_board.get_piece(i, j)

    # print(i, j)


def release(event):
    x, y = event.x, event.y
    ox, oy = pixel_to_index(x, y)
    C.target = ox, oy
    C.send()
    v_board.selected_piece.set_coord(pixel_to_square(x, y))
    v_board.selected_piece = None


root.bind('<ButtonPress-1>', click)
root.bind('<B1-Motion>', drag)
root.bind('<ButtonRelease-1>', release)
# root.bind('<Button-1>', motion)
# root.bind('<Motion>', motion)




# x, y = index_to_square(piece['x'], piece['y'])
# canvas.create_text(x, y, anchor="center", text='C', fill='white', font='helvetica 35')


while True:
    # x, y = piece['x'], piece['y']
    # x, y = index_to_square(piece['x'], piece['y'])
    # print(x, y)
    canvas.delete('all')
    # draw_grid()
    # canvas.create_text(x, y, anchor="center", text='C', fill='white', font='helvetica 35')
    draw_grid()
    draw_board()
    canvas.update()

# root.mainloop()




mainloop()