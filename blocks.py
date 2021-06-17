from math import floor
from random import randint


def log(text=""):
    log = False
    if log:
        print(text)


class Block():
    """Class that represents blocks in tetris"""

    def __init__(self, shape: int = 1) -> None:
        """Arguments:\n
            shape - shape of blok (default 0), values:
                0 - long block
                1 - square block
                2 - "L" left block
                3 - "L" right block
                4 - "Z" left block
                5 - "Z" right block
            color - (r,g,b) tupple of rgb values (default (255,0,0))
        """
        self._positions = []
        self.shape = shape
        self._color, self._dead_color = (0, 0, 0), (0, 0, 0)
        self._facing = 0

    def __repr__(self) -> str:
        fields = tuple("{}={}".format(k, v) for k, v in self.__dict__.items())
        return self.__class__.__name__ + str(tuple(sorted(fields))).replace("\'", "")

    @property
    def shape(self) -> int:
        return self._shape

    @property
    def facing(self) -> int:
        return self._facing

    @property
    def color(self) -> tuple:
        return self._color

    @property
    def dead_color(self) -> tuple:
        return self._dead_color

    @property
    def positions(self) -> list:
        return self._positions

    @shape.setter
    def shape(self, newShape: int) -> None:
        if not isinstance(newShape, int) or newShape < 0 or newShape > 5:
            self._shape = 0
        else:
            self._shape = newShape

    def reset_positions(self, game_size: tuple, height: int = 4) -> None:
        self._positions = [floor(game_size[0]/2), height]

    def _handle_change_side(self, clockwise: bool = False) -> int:
        """Rotates the block"""
        log("rotating from " + str(self._facing))
        face = self._facing
        if not clockwise:
            face += 1
            if face > 1 and self._shape in (0, 1, 5):
                face = 0
            elif face > 3:
                face = 0
        else:
            face -= 1
            if face < 0 and self._shape in (0, 1, 5):
                face = 1
            elif face < 0:
                face = 3
        return face

    def _handle_fall(self) -> list:
        ret = []
        for x in range(4):
            ret.append([self._positions[x][0], self._positions[x][1]+1])
        return ret

    def _handle_move(self, side) -> list:
        ret = []
        if side == "left":
            for x in range(4):
                ret.append([self._positions[x][0]-1, self._positions[x][1]])
        else:
            for x in range(4):
                ret.append([self._positions[x][0]+1, self._positions[x][1]])
        return ret

    def move(self, side, dry_run=False,  game_array=[], game_size=()):
        """
        Method used to move the blocks
        side=string(left/right)
        if dry_run=True then method checks if next position is correct and takes additional params:
              game_array=array[[]] - game array
              block_positions=array[tupple(x,y)] - current positions
              game_size=tuple(int,int) - size of game array
       """
        ret = True
        new_pos = self._handle_move(side)
        # vertical
        if dry_run:
            for x in new_pos:
                if x[0] < 0 or x[0] > game_size[0]-1 or x[1] > game_size[1]:
                    ret = False
                elif game_array[x[0]][x[1]] == 2:
                    ret = False
        else:
            log(new_pos)
            self._positions = new_pos
        return ret

    def fall(self, dry_run=False,  game_array=[], game_size=()):
        """
        Method used to make the blocks fall
        if dry_run=True then method checks if next position is correct and takes additional params:
              game_array=array[[]] - game array
              block_positions=array[tupple(x,y)] - current positions
              game_size=tuple(int,int) - size of game array
       """
        ret = True
        new_pos = self._handle_fall()
        # vertical
        if dry_run:
            for x in new_pos:
                if x[0] < 0 or x[0] >= game_size[0] or x[1] >= game_size[1]:
                    ret = False
                elif game_array[x[0]][x[1]] == 2:
                    ret = False
        else:
            log(new_pos)
            self._positions = new_pos
        return ret

    def rotate(self, dry_run=False, game_array=[], game_size=()):
        """
        Method used to rotate the blocks
            if dry_run=True then method checks if next position is correct and takes additional params:
                game_array=array[[]] - game array
                game_size=tuple(int,int) - size of game array
        """
        pass


class Long_Block(Block):
    def __init__(self):
        super().__init__(0)
        self._color, self._dead_color = (247, 23, 7), (156, 48, 40)

    def rotate(self,  dry_run=False, game_array=[], game_size=()):
        """
       Method used to rotate the blocks
          if dry_run=True then method checks if next position is correct and takes additional params:
              game_array=array[[]] - game array
              game_size=tuple(int,int) - size of game array
       """
        ret = True
        bp = self._positions  # shorter syntax
        new_pos = []

        new_face = self._handle_change_side()
        if new_face == 0:
            # vertical
            new_pos.append((bp[0][0]-1, bp[0][1]-1))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0]+1, bp[2][1]+1))
            new_pos.append((bp[3][0]+2, bp[3][1]+2))

        else:  # new_face == 1
            # horizontal
            new_pos.append((bp[0][0]+1, bp[0][1]+1))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0]-1, bp[2][1]-1))
            new_pos.append((bp[3][0]-2, bp[3][1]-2))
        if dry_run:
            for x in new_pos:
                if x[0] < 0 or x[0] >= game_size[0] or x[1] >= game_size[1]:
                    ret = False
                elif game_array[x[0]][x[1]] == 2:
                    ret = False
        else:
            self._positions = new_pos
            self._facing = new_face
        return ret

    def reset_positions(self, game_size, height=4):
        log(str(game_size))
        self._positions = []
        self._positions.append((floor(game_size[0]/2), height))
        self._positions.append((self._positions[0][0], height+1))
        self._positions.append((self._positions[1][0], height+2))
        self._positions.append((self._positions[2][0], height+3))


class square_block(Block):
    def __init__(self):
        super().__init__(1)
        self._color, self._dead_color = (245, 241, 24), (194, 192, 74)

    def reset_positions(self, game_size, height=4):
        self._positions = []
        self._positions.append((floor(game_size[0]/2), height))
        self._positions.append((self._positions[0][0]+1, height+1))
        self._positions.append((self._positions[1][0], height))
        self._positions.append((self._positions[0][0], height+1))


class L_block_l(Block):
    def __init__(self):
        super().__init__(2)
        self._color, self._dead_color = (41, 240, 19), (77, 186, 65)

    def rotate(self,  dry_run=False, game_array=[], game_size=()):
        """
       Method used to rotate the blocks
          if dry_run=True then method checks if next position is correct and takes additional params:
              game_array=array[[]] - game array
              game_size=tuple(int,int) - size of game array
       """
        ret = True
        bp = self._positions  # shorter syntax
        new_pos = []

        new_face = self._handle_change_side()
        if new_face == 0:
            # vertical
            new_pos.append((bp[0][0]-1, bp[0][1]-1))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0]+1, bp[2][1]+1))
            new_pos.append((bp[3][0], bp[3][1]+2))

        elif new_face == 1:
            # horizontal
            new_pos.append((bp[0][0]-1, bp[0][1]+1))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0]+1, bp[2][1]-1))
            new_pos.append((bp[3][0]+2, bp[3][1]))

        elif new_face == 2:
            # horizontal
            new_pos.append((bp[0][0]+1, bp[0][1]+1))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0]-1, bp[2][1]-1))
            new_pos.append((bp[3][0], bp[3][1]-2))

        else:  # new_face==3
            # horizontal
            new_pos.append((bp[0][0]+1, bp[0][1]-1))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0]-1, bp[2][1]+1))
            new_pos.append((bp[3][0]-2, bp[3][1]))
        if dry_run:
            for x in new_pos:
                if x[0] < 0 or x[0] >= game_size[0] or x[1] >= game_size[1]:
                    ret = False
                elif game_array[x[0]][x[1]] == 2:
                    ret = False
        else:
            self._positions = new_pos
            self._facing = new_face
        return ret

    def reset_positions(self, game_size, height=4):
        log("game size: "+str(game_size))
        self._positions = []
        self._positions.append((floor(game_size[0]/2), height-1))
        self._positions.append((self._positions[0][0], height))
        self._positions.append((self._positions[1][0], height+1))
        self._positions.append((self._positions[2][0]-1, height+1))
        log("kekw: " + str(self._positions))


class L_block_r(Block):
    def __init__(self):
        super().__init__(3)
        self._color, self._dead_color = (37, 245, 203), (58, 140, 124)

    def rotate(self,  dry_run=False, game_array=[], game_size=()):
        """
        Method used to rotate the blocks
          if dry_run=True then method checks if next position is correct and takes additional params:
              game_array=array[[]] - game array
              game_size=tuple(int,int) - size of game array
        """
        ret = True
        bp = self._positions  # shorter syntax
        new_pos = []

        new_face = self._handle_change_side()
        if new_face == 0:
            # vertical
            new_pos.append((bp[0][0]-1, bp[0][1]-1))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0]+1, bp[2][1]+1))
            new_pos.append((bp[3][0]+2, bp[3][1]))

        elif new_face == 1:
            # horizontal
            new_pos.append((bp[0][0]-1, bp[0][1]+1))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0]+1, bp[2][1]-1))
            new_pos.append((bp[3][0], bp[3][1]-2))
        elif new_face == 2:
            # horizontal
            new_pos.append((bp[0][0]+1, bp[0][1]+1))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0]-1, bp[2][1]-1))
            new_pos.append((bp[3][0]-2, bp[3][1]))

        else:  # new_face==3
            # horizontal
            new_pos.append((bp[0][0]+1, bp[0][1]-1))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0]-1, bp[2][1]+1))
            new_pos.append((bp[3][0], bp[3][1]+2))
        if dry_run:
            for x in new_pos:
                if x[0] < 0 or x[0] >= game_size[0] or x[1] >= game_size[1]:
                    ret = False
                elif game_array[x[0]][x[1]] == 2:
                    ret = False
        else:
            self._positions = new_pos
            self._facing = new_face
        return ret

    def reset_positions(self, game_size, height=4):
        self._positions = []
        self._positions.append((floor(game_size[0]/2), height-1))
        self._positions.append((self._positions[0][0], height))
        self._positions.append((self._positions[1][0], height+1))
        self._positions.append((self._positions[2][0]+1, height+1))


class Z_block_l(Block):
    def __init__(self):
        super().__init__(4)
        self._color, self._dead_color = (20, 61, 245), (58, 72, 135)

    def rotate(self,  dry_run=False, game_array=[], game_size=()):
        """
       Method used to rotate the blocks
          if dry_run=True then method checks if next position is correct and takes additional params:
              game_array=array[[]] - game array
              game_size=tuple(int,int) - size of game array
       """
        ret = True
        bp = self._positions  # shorter syntax
        new_pos = []

        new_face = self._handle_change_side()
        if new_face == 0:
            # horizontal
            new_pos.append((bp[0][0], bp[0][1]-2))
            new_pos.append((bp[1][0]+1, bp[1][1]-1))
            new_pos.append((bp[2][0], bp[2][1]))
            new_pos.append((bp[3][0]+1, bp[3][1]+1))

        elif new_face == 1:
            # vertical
            new_pos.append((bp[0][0]+2, bp[0][1]))
            new_pos.append((bp[1][0]+1, bp[1][1]+1))
            new_pos.append((bp[2][0], bp[2][1]))
            new_pos.append((bp[3][0]-1, bp[3][1]+1))
        elif new_face == 2:
            # horizontal
            new_pos.append((bp[0][0], bp[0][1]+2))
            new_pos.append((bp[1][0]-1, bp[1][1]+1))
            new_pos.append((bp[2][0], bp[2][1]))
            new_pos.append((bp[3][0]-1, bp[3][1]-1))
        else:  # new_face == 3:
            # vertcal
            new_pos.append((bp[0][0]-2, bp[0][1]))
            new_pos.append((bp[1][0]-1, bp[1][1]-1))
            new_pos.append((bp[2][0], bp[2][1]))
            new_pos.append((bp[3][0]+1, bp[3][1]-1))

        if dry_run:
            for x in new_pos:
                if x[0] < 0 or x[0] >= game_size[0] or x[1] >= game_size[1]:
                    ret = False
        else:
            self._positions = new_pos
            self._facing = new_face
        return ret

    def reset_positions(self, game_size, height=4):
        self._positions = []
        self._positions.append((floor(game_size[0]/2)-1, height))
        self._positions.append((self._positions[0][0]+1, height))
        self._positions.append((self._positions[1][0], height+1))
        self._positions.append((self._positions[2][0]+1, height+1))


class Z_block_r(Block):
    def __init__(self):
        super().__init__(5)
        self._color, self._dead_color = (255, 41, 251), (140, 56, 139)

    def rotate(self,  dry_run=False, game_array=[], game_size=()):
        """
       Method used to rotate the blocks
          if dry_run=True then method checks if next position is correct and takes additional params:
              game_array=array[[]] - game array
              game_size=tuple(int,int) - size of game array
       """
        ret = True
        bp = self._positions  # shorter syntax
        new_pos = []

        new_face = self._handle_change_side()
        if new_face == 0:
            # vertical
            new_pos.append((bp[0][0], bp[0][1]))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0], bp[2][1]-2))
            new_pos.append((bp[3][0]+2, bp[3][1]))

        else:  # new_face == 1
            # horizontal
            new_pos.append((bp[0][0], bp[0][1]))
            new_pos.append((bp[1][0], bp[1][1]))
            new_pos.append((bp[2][0], bp[2][1]+2))
            new_pos.append((bp[3][0]-2, bp[3][1]))
        if dry_run:
            for x in new_pos:
                if x[0] < 0 or x[0] >= game_size[0] or x[1] >= game_size[1]:
                    ret = False
                elif game_array[x[0]][x[1]] == 2:
                    ret = False
        else:
            self._positions = new_pos
            self._facing = new_face
        return ret

    def reset_positions(self, game_size, height=4):
        self._positions = []
        self._positions.append((floor(game_size[0]/2)-1, height))
        self._positions.append((self._positions[0][0]+1, height))
        self._positions.append((self._positions[1][0], height+-1))
        self._positions.append((self._positions[2][0]+1, height-1))


if __name__ == "__main__":
    block = Block(shape=-2)
    x = (3, 4)
    print(block)
    print(type(x))
