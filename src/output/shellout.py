from src.output.utils import Utils


class Shellout:
    """
    Handels all the Conversion from Application to String
    The Application must be horizontal
    """
    matrix = []
    omatrix = []
    width = 0
    height = 0

    __pixels = object

    def __init__(self, width: int, height: int):
        self.colors = []

        self.width = int(width)
        self.height = int(height)

        self.utils = Utils()

        self.matrix = [[(0, 0, 0) for _ in range(self.height)] for _ in range(self.width)]
        self.omatrix = [[(0, 0, 0) for _ in range(self.height)] for _ in range(self.width)]

    def __getitem__(self, item):
        if len(item) != 2:
            raise ValueError('Index needs two values example: [1, 2]')
        return self.matrix[item[0]][item[1]]

    def __setitem__(self, key, value):
        if len(key) != 2:
            raise ValueError('Index needs two values example: [1, 2]')
        self.matrix[key[0]][key[1]] = value

    def submit_all(self):
        """
        Writes all the changes to tne Neopixel String
        """
        for row in self.matrix:
            print(self.get_out(row))
        print("--------------------------------------------------------------------------------------------")

    def get_out(self, row):
        ret_row = []
        for color in row:
            if color not in self.colors:
                self.colors.append(color)
            ret_row.append(self.colors.index(color))
        return ret_row

    def fill_all(self, color: tuple):
        """
        Fills sets all the Pixels to the specified color
        :param color: needs to be a tripel with RGB values example: (255, 6, 187)
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = color
        print('Fill: ' + str(color))

    def set_matrix(self, matrix):
        """
        Replace the matrix
        :param matrix: new 2dim tupel array must be same lengh as old one
        :return: true if lengh is right, false if not
        """
        if len(matrix) != len(self.matrix):
            return False
        else:
            if len(matrix[0]) != len(self.matrix[0]):
                return False
            else:
                self.matrix = matrix
                return True
