import copy
import tkinter

import numpy as np
from PIL import ImageTk, Image

import Constants
from board.src.Position import Position


class Gui:
    ranks = 8
    files = 8
    total_squares = 64
    top_padding = ranks * total_squares * 0.125  # To  vertically center the board

    images = []

    def __init__(self, parent, position):
        self.parent = parent

        # Creating Canvas
        canvas_width = (self.files * self.total_squares) * 1.5  # Extra area for the menu
        canvas_height = self.ranks * self.total_squares * 1.25
        self.canvas = tkinter.Canvas(parent, width=canvas_width, height=canvas_height, background="white")
        self.canvas.pack(padx=8, pady=8)  # Padding to the border of the window

        # Creating the pieces
        width = height = self.total_squares
        red_man_icon = Image.open(Constants.RED_MAN_ICON).resize((width, height), Image.ANTIALIAS)
        red_king_icon = Image.open(Constants.RED_KING_ICON).resize((width, height), Image.ANTIALIAS)
        white_man_icon = Image.open(Constants.WHITE_MAN_ICON).resize((width, height), Image.ANTIALIAS)
        white_king_icon = Image.open(Constants.WHITE_KING_ICON).resize((width, height), Image.ANTIALIAS)

        self.images.append(ImageTk.PhotoImage(red_man_icon))
        self.images.append(ImageTk.PhotoImage(red_king_icon))
        self.images.append(ImageTk.PhotoImage(white_man_icon))
        self.images.append(ImageTk.PhotoImage(white_king_icon))

        # Drawing the board and the pieces
        self.draw_board()
        self.draw_pieces(position)

    # Right side panel with he information of the performed moves
    def draw_moves_panel(self):
        pass

    def draw_menu_buttons(self):
        pass

    def draw_new_game_button(self):
        pass

    def draw_save_button(self):
        pass

    def draw_load_button(self):
        pass

    def draw_restart_button(self):
        pass

    def draw_board(self):

        color = Constants.BLACK_COLOR

        for rank in range(self.ranks):

            for file in range(self.files):

                # Top-left corner of the square
                x1 = file * self.total_squares
                y1 = ((7 - rank) * self.total_squares) + self.top_padding

                # Bottom-right corner of the square
                x2 = x1 + self.total_squares
                y2 = y1 + self.total_squares

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="square")

                if file != 7:  # Color change for the next square
                    color = Constants.WHITE_COLOR if (color == Constants.BLACK_COLOR) else Constants.BLACK_COLOR

    def draw_pieces(self, position):

        tmp_position = copy.deepcopy(position)

        red_men = tmp_position.red_men()
        red_kings = tmp_position.red_kings()
        white_men = tmp_position.white_men()
        white_kings = tmp_position.white_kings()

        # Delete current board
        self.canvas.delete("occupied")
        self.iterate_bitboard(red_men, Constants.RED_MAN)
        self.iterate_bitboard(red_kings, Constants.RED_KING)
        self.iterate_bitboard(white_men, Constants.WHITE_MAN)
        self.iterate_bitboard(white_kings, Constants.WHITE_KING)

    def iterate_bitboard(self, bitboard, piece_type):

        index = 0
        while bitboard:  # If red_men == 0, it is empty or all indexes where checked

            if bitboard & Constants.MSB_SET:  # equivalent to bitboard & 0b1000000...
                self.draw_piece(index, piece_type)

            bitboard = np.uint32(bitboard << 1)
            index += 1

    def draw_piece(self, index, piece_type):
        file = Position.get_file_from_index(index) - 1
        rank = Position.get_rank_from_index(index) - 1

        piece_name = "%s_%d_%d" % (piece_type, file, rank)
        x = (file * self.total_squares) + int(self.total_squares / 2)
        y = ((7 - rank) * self.total_squares) + int(self.total_squares / 2) + self.top_padding

        # Selection of the proper icon
        if piece_type == Constants.RED_MAN:
            icon = self.images[0]
        elif piece_type == Constants.RED_KING:
            icon = self.images[1]
        elif piece_type == Constants.WHITE_MAN:
            icon = self.images[2]
        else:
            icon = self.images[3]

        # Adding the image to the canvas
        self.canvas.create_image(x, y, image=icon, tags=(piece_name, "occupied"), anchor="center")


#################


def main():
    window = tkinter.Tk()
    window.title("Emily - Draughts Engine")
    gui = Gui(window, Position.initial_position())
    window.mainloop()


if __name__ == "__main__":
    main()
