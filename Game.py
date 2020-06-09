import pygame
import random

pygame.init()

pygame.display.set_caption("                                                                       SUDOKU")

WIDTH = 560
HEIGHT = WIDTH + 100
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
run = True


class Sudoku:
    global WIDTH, HEIGHT, position, active, field  # should have made an variable SIDE = WIDTH - 20 ... but i didnt lol
    line_x = 10
    line_y = 10

    def __init__(self):
        self.text = None
        self.text_x = 10
        self.text_y = 10
        self.row = 9
        self.pos_opt_x = None
        self.pos_opt_y = None
        self.field_position = None
        self.font = pygame.font.SysFont('comicsans', 10, True)  # art, größe, bold, italic

    def drawBackground(self):
        pygame.draw.rect(window, (255, 255, 255), (0, 0, WIDTH, HEIGHT))

    def drawGrid(self):
        for i in range(10):
            pygame.draw.line(window, (0, 0, 0), (self.line_x, self.line_y + ((WIDTH - 20) / 9) * i),
                             (self.line_x + WIDTH - 20, self.line_y + ((WIDTH - 20) / 9) * i))
        for i in range(10):
            pygame.draw.line(window, (0, 0, 0), (self.line_x + ((WIDTH - 20) / 9) * i, self.line_y),
                             (self.line_x + ((WIDTH - 20) / 9) * i, self.line_y + WIDTH - 20))

    def drawSudokuEdge(self):
        pygame.draw.rect(window, (0, 0, 0), (self.line_x, self.line_y, WIDTH - 20, WIDTH - 20), 4)

    def drawSquares(self):
        for i in range(3):
            for p in range(3):
                pygame.draw.rect(window, (0, 0, 0),
                                 (self.line_x + ((WIDTH - 20) / 3) * i, self.line_y + ((WIDTH - 20) / 3) * p,
                                  ((WIDTH - 20) / 3), ((WIDTH - 20) / 3)), 2)

    def drawCurrentField(self):
        if active:
            pygame.draw.rect(window, (255, 165, 0),
                             (self.pos_opt_x, self.pos_opt_y, (WIDTH - 20) / 9, (WIDTH - 20) / 9), 3)

    def logicPositionOptimized(self):
        for i in range(10):
            if 10 < position[0] < 10 + 60 * i:
                self.pos_opt_x = 10 + 60 * (i - 1)
                break
        for i in range(10):
            if 10 < position[1] < 10 + 60 * i:
                self.pos_opt_y = 10 + 60 * (i - 1)
                break

    def logicPositionField(self):  # 0 1 2 3 4 5 6 7 8 / 9 10 11 12 13 14 15 16 17 / ...
        self.field_position = ((self.pos_opt_x - 10) // 60) + (9 * (self.pos_opt_y - 10) // 60)  # einser + zehner
        return self.field_position


class Number:
    font_gray = pygame.font.SysFont('comicsans', 30, True)  # art, größe, bold, italic
    font_black = pygame.font.SysFont('comicsans', 80, True)

    def __init__(self, pos_opt_x, pos_opt_y, input_num, enter):
        self.pos_opt_x = pos_opt_x
        self.pos_opt_y = pos_opt_y

        self.input_num = input_num

        self.text_gray_x = self.pos_opt_x + 5
        self.text_gray_y = self.pos_opt_y + 5
        self.text_gray = self.font_gray.render(str(self.input_num), 1, (128, 128, 128))

        self.text_black = self.font_black.render(str(self.input_num), 1, (0, 0, 0))
        self.text_black_x = self.pos_opt_x + 12
        self.text_black_y = self.pos_opt_y + 12
        self.enter = enter

    def drawNumberGray(self):
        if not self.enter:
            window.blit(self.text_gray, (self.text_gray_x, self.text_gray_y))

    def drawNumberBlack(self):
        if self.enter:
            window.blit(self.text_black, (self.text_black_x, self.text_gray_y))


s = Sudoku()
active = False
field_active = False
field = []
x = 0
y = 0
key_pressed = False
for i in range(9):
    field.append([0 for z in range(9)])
time = 0
Numbers = []
for i in range(81):
    Numbers.append(0)
input_num = 0


def rules(field, test_number, row, column):
    if test_number in field[row]:
        return False
    for i in range(9):
        if field[i][column] == test_number:
            return False
    x_start = (row // 3) * 3
    x_end_inclusive = x_start + 2
    y_start = (column // 3) * 3
    y_end_inclusive = y_start + 2
    for x in range(x_start, x_end_inclusive + 1):  # +1 weil range bis einen davor geht und die variable eigentlich
        for y in range(y_start, y_end_inclusive + 1):  # schon die letzte zu prüfende position enthält
            if x == row and y == column:
                continue
            if field[x][y] == test_number:
                return False
    return True


def find(field):
    for x in range(9):
        for y in range(9):
            if field[x][y] == 0:
                return x, y
    return False


def solve(field):
    found = find(field)
    if not found:
        return True
    else:
        row, column = found
    for n in range(1, 10):
        if rules(field, n, row, column):
            field[row][column] = n
            print(field)
            if solve(field):
                return True
            field[row][column] = 0
    return False


def redrawGameWindow():
    s.drawBackground()
    s.drawGrid()
    s.drawSudokuEdge()
    s.drawSquares()
    s.drawCurrentField()
    for f in range(9):
        for i in range(9):
            if field[f][i] != 0:
                Numbers[f * 9 + i] = Number(10 + 60 * i, 10 + 60 * f, field[f][i], enter=True)
    for N in Numbers:
        if N != 0:
            N.drawNumberGray()
            N.drawNumberBlack()
    pygame.display.update()


while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()  # returns a tuple of booleans in this order (leftclick, middleclick, rightclick)

    if mouse[0]:
        position = pygame.mouse.get_pos()
        s.logicPositionOptimized()
        active = True

    if keys[pygame.K_UP]:
        if s.pos_opt_y is None:
            s.pos_opt_y = 10
            s.pos_opt_x = 10
            active = True
        if s.pos_opt_y >= 10 + 60:
            if time == 0:
                time = 3
                s.pos_opt_y -= 60

    if keys[pygame.K_DOWN]:
        if s.pos_opt_y is None:
            s.pos_opt_y = 10
            s.pos_opt_x = 10
            active = True
        if s.pos_opt_y < WIDTH - 10 - 60:
            if time == 0:
                time = 3
                s.pos_opt_y += 60

    if keys[pygame.K_LEFT]:
        if s.pos_opt_y is None:
            s.pos_opt_y = 10
            s.pos_opt_x = 10
            active = True
        if s.pos_opt_x >= 10 + 60:
            if time == 0:
                time = 3
                s.pos_opt_x -= 60

    if keys[pygame.K_RIGHT]:
        if s.pos_opt_y is None:
            s.pos_opt_y = 10
            s.pos_opt_x = 10
            active = True
        if s.pos_opt_x < WIDTH - 10 - 60:
            if time == 0:
                time = 3
                s.pos_opt_x += 60

    if keys[pygame.K_SPACE]:
        field_active = True
        solve(field)

    if active:
        if keys[pygame.K_1] or keys[pygame.K_KP1]:
            input_num = 1
            key_pressed = True
        if keys[pygame.K_2] or keys[pygame.K_KP2]:
            input_num = 2
            key_pressed = True
        if keys[pygame.K_3] or keys[pygame.K_KP3]:
            input_num = 3
            key_pressed = True
        if keys[pygame.K_4] or keys[pygame.K_KP4]:
            input_num = 4
            key_pressed = True
        if keys[pygame.K_5] or keys[pygame.K_KP5]:
            input_num = 5
            key_pressed = True
        if keys[pygame.K_6] or keys[pygame.K_KP6]:
            input_num = 6
            key_pressed = True
        if keys[pygame.K_7] or keys[pygame.K_KP7]:
            input_num = 7
            key_pressed = True
        if keys[pygame.K_8] or keys[pygame.K_KP8]:
            input_num = 8
            key_pressed = True
        if keys[pygame.K_9] or keys[pygame.K_KP9]:
            input_num = 9
            key_pressed = True

        field_row = s.logicPositionField() // 9
        field_column = s.logicPositionField() % 9

        if key_pressed:
            if active:
                enter = False
                Numbers[s.logicPositionField()] = Number(s.pos_opt_x, s.pos_opt_y, input_num, enter)
            key_pressed = False

        if keys[pygame.K_BACKSPACE] and Numbers[s.logicPositionField()] != 0:
            Numbers[s.logicPositionField()] = 0
            field[field_row][field_column] = 0
            enter = False

        if (keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]) and Numbers[s.logicPositionField()] != 0 \
                and Numbers[s.logicPositionField()].input_num != field[field_row][field_column]:

            if not rules(field, Numbers[s.logicPositionField()].input_num, field_row, field_column):
                field[field_row][field_column] = 0
                Numbers[s.logicPositionField()] = 0
            else:
                Numbers[s.logicPositionField()].enter = True
                field[field_row][field_column] = Numbers[s.logicPositionField()].input_num

    if time > 0:
        time -= 1
    redrawGameWindow()
pygame.quit()
