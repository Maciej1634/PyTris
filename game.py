from math import floor
from random import randint
import blocks


def log(text=""):
    log = False
    if log:
        print(text)


class Tetris():
    """
    Class representing the classic tetris game
        params:
        game_size=tupple(int,int) - size of game grid
        screen_size=tupple(int,int) - size of game screen
    """

    def __init__(self, game_size=(16, 11), small_grid_size=(5, 5)):
        self._game_size = game_size
        self._small_grid_size = small_grid_size
        self._game_array = []
        self._active_block = blocks.Block()
        self._next_block = blocks.Block()
        self._points = 0
        self._color_mask = []
        self._rotate = False
        self.small_grid_default_pos = 2
        self._move = "nope"
        self._default_height = 1
        self._max_row = 0

    def __repr__(self) -> str:
        fields = tuple("{}={}".format(k, v) for k, v in self.__dict__.items())
        return self.__class__.__name__ + str(tuple(sorted(fields))).replace("\'", "")

    @property
    def game_size(self):
        return self._game_size

    @property
    def active_color(self):
        return self._active_block.color

    @property
    def game_array(self):
        return self._game_array

    @property
    def color_mask(self):
        ret = self.game_array
        for x in range(self._game_size[0]):
            for y in range(self._game_size[1]):
                if self._game_array[x][y] == 1:
                    ret[x][y] = self._active_block.color
                if self._game_array[x][y] == 2:
                    ret[x][y] = self._color_mask
        return ret

    @property
    def small_block_pos(self):
        return self._next_block.positions

    @property
    def points(self):
        return self._points

    def get_pos_color(self, x, y) -> tuple:
        """
        return color_mask[x][y]
        """
        return self._color_mask[x][y]

    def init_game(self) -> None:
        """first call of game"""
        log("init_game")
        self._calc_max_row()
        self.small_grid_default_pos = floor(self._small_grid_size[1]/2)
        self._game_array = [
            [0 for x in range(self._game_size[1])] for y in range(self._game_size[0])]
        self._color_mask = [
            [0 for x in range(self._game_size[1])] for y in range(self._game_size[0])]
        self._active_block = blocks.Long_Block()
        self._next_block = blocks.L_block_l()
        self._reset_position()
        self._change_current_position_array_values(1)
        self._update_color_mask()
        self._next_block.reset_positions(
            self._small_grid_size, self.small_grid_default_pos)

    def nex_game_tick(self) -> None:
        """Calculate the next iteration of game"""
        log("next game tick - start")

        self._change_current_position_array_values(0)
        self._handle_fall()
        self._change_current_position_array_values(1)
        self._update_color_mask()

    def _reset_position(self):
        log("_reset_position")
        self._active_block.reset_positions(self.game_size)

    def _handle_next_block(self):
        log("_handle_next_block")
        self._active_block = self._next_block
        self._active_block.reset_positions(
            self._game_size, height=self._default_height)
        b = randint(0, 5)
        if b == 0:
            self._next_block = blocks.Long_Block()
        elif b == 1:
            self._next_block = blocks.square_block()
        elif b == 2:
            self._next_block = blocks.L_block_l()
        elif b == 3:
            self._next_block = blocks.L_block_r()
        elif b == 4:
            self._next_block = blocks.Z_block_l()
        elif b == 5:
            self._next_block = blocks.Z_block_r()
        self._next_block.reset_positions(
            self._small_grid_size, self.small_grid_default_pos)

    def _change_current_position_array_values(self, value: int):
        log("_change_current_position_array_values "+str(value))
        for i in self._active_block.positions:
            self._game_array[i[0]][i[1]] = value

    def _handle_hit(self):
        """
        type=string(move/rotate)
        """
        log("_handle_hit")
        self._update_color_mask(True)
        self._change_current_position_array_values(2)
        if self._check_destroyable_rows():
            self._handle_destroy_rows()
        self._handle_next_block()

    def _update_color_mask(self, is_dead=False):
        if is_dead:
            for i in self._active_block.positions:
                self._color_mask[i[0]][i[1]] = self._active_block.dead_color
        else:
            for i in self._active_block.positions:
                self._color_mask[i[0]][i[1]] = self._active_block.color

    def _handle_destroy_rows(self):
        d_arr = self._check_destroyable_rows(True)
        c = len(d_arr)
        if c == 1:
            self._points += 100
        elif c == 2:
            self._points += 200
        elif c == 3:
            self._points += 300
        elif c == 4:
            self._points += 1000
        self._destroy_rows(d_arr)

    def _destroy_rows(self, to_destroy):
        log("destroy: "+str(to_destroy))
        for x in to_destroy:
            self._change_row(x, 0)
        for x in to_destroy:
            for i in range(x, 0, -1):
                log(str(x)+" "+str(i))
                self._change_rows_places(i, i-1)

    def _change_row(self, row, value):
        for x in range(self._game_size[0]):
            self._game_array[x][row] = value

    def _change_rows_places(self, row, row2):
        for x in range(self._game_size[0]):
            self._game_array[x][row], self._game_array[x][row2] = self._game_array[x][row2], self._game_array[x][row]

    def _sum_row(self, row):
        s = 0
        for x in range(self._game_size[0]):
            s += self._game_array[x][row]
        log("sum row: "+str(s))
        return s

    def _calc_max_row(self):
        if self.game_size[1] % 2 == 1:
            self._max_row = self._game_size[0]*2-1
        else:
            self._max_row = self._game_size[0]*2

    def _check_destroyable_rows(self, send_to_array=False):
        ret = False
        c = []
        for x in range(self._game_size[1]):
            if self._sum_row(x) >= self._max_row:
                if send_to_array:
                    c.append(x)
                else:
                    ret = True
        log("destroyable: " + str(ret))
        return c if send_to_array else ret

    def rotate_block(self):
        """Rotate the active block"""
        self._rotate = True

    def move_block(self, side="left"):
        self._move = side

    def _handle_fall(self):
        if self._move == "left":
            self._move = "nope"
            if self._active_block.move("left", dry_run=True, game_array=self._game_array, game_size=self._game_size):
                self._active_block.move("left")
        elif self._move == "right":
            self._move = "nope"
            if self._active_block.move("right", dry_run=True, game_array=self._game_array, game_size=self._game_size):
                self._active_block.move("right")
        if self._rotate:
            if self._active_block.rotate(dry_run=True, game_array=self._game_array, game_size=self._game_size):
                self._active_block.rotate()
            self._rotate = False
        if self._active_block.fall(dry_run=True, game_array=self._game_array, game_size=self._game_size):
            self._active_block.fall()
        else:
            self._handle_hit()


if __name__ == "__main__":

    game = Tetris((16, 11), (5, 4))
    print(repr(game))
