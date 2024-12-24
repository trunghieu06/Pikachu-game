import pygame
import random
import sys
import os
import glob

# Màu sắc (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0) 
path = [i.replace('\\', '/') for i in glob.glob('./DataSet/*.png')]
background_img = pygame.image.load('background.png')
back_button = pygame.image.load('back_button.png')
hint_button = pygame.image.load('hint_button.png')
NO_IMAGE = len(path)
IMAGE_SIZE = (50, 40)
width, height = 1200, 700

def draw_button(screen, img, x, y):
    screen.blit(img, (x, y))

class Grid:
    def __init__(self, ROW, COL):
        self.ROW = ROW
        self.COL = COL
        self.ROW = min(self.ROW, 12)
        self.COL = min(self.COL, 24)
        self.grid = [[-1] * (COL + 3) for _ in range(ROW + 3)]
        self.cods = [[-1] * (COL + 3) for _ in range(ROW + 3)]
        self.grid_button = [[pygame.Rect(0, 0, 0, 0)] * (COL) for _ in range(ROW)]
        x = (700 - ROW * IMAGE_SIZE[0]) // 2
        for i in range(ROW):
            y = (1200 - COL * IMAGE_SIZE[1]) // 2
            for j in range(COL):
                self.grid_button[i][j] = pygame.Rect(y, x, IMAGE_SIZE[1], IMAGE_SIZE[0])
                self.cods[i + 1][j + 1] = (y + IMAGE_SIZE[1] // 2, x + IMAGE_SIZE[0] // 2)
                y += IMAGE_SIZE[1]
            x += IMAGE_SIZE[0]
        for i in range(1, COL + 1):
            self.cods[0][i] = (self.cods[1][i][0], self.cods[1][i][1] - IMAGE_SIZE[0])
            self.cods[ROW + 1][i] = (self.cods[ROW][i][0], self.cods[ROW][i][1] + IMAGE_SIZE[0])
        for i in range(1, ROW + 1):
            self.cods[i][0] = (self.cods[i][1][0] - IMAGE_SIZE[1], self.cods[i][1][1])
            self.cods[i][COL + 1] = (self.cods[i][COL][0] + IMAGE_SIZE[1], self.cods[i][COL][1])
    def set_grid(self, grid):
        self.grid = grid
    def reset_grid(self):
        pre_img = random.randint(0, NO_IMAGE - 1)
        cnt = 1
        self.grid[1][1] = pre_img
        
        while cnt < self.ROW * self.COL:
            i, j = random.randint(1, self.ROW), random.randint(1, self.COL)
            while self.grid[i][j] != -1:
                i, j = random.randint(1, self.ROW), random.randint(1, self.COL)
            self.grid[i][j] = pre_img
            if cnt == self.ROW * self.COL - 1:
                break
            pre_img = random.randint(0, NO_IMAGE - 1)
            while self.grid[i][j] != -1:
                i, j = random.randint(1, self.ROW), random.randint(1, self.COL)
            self.grid[i][j] = pre_img
            cnt += 2
    def check_1(self, pt1, pt2):
        # 2 cases
        if pt1[0] == pt2[0]:
            if pt1[1] > pt2[1]:
                pt1, pt2 = pt2, pt1
            for i in range(pt1[1] + 1, pt2[1]):
                if self.grid[pt1[0]][i] != -1:
                    return False
            return True
        elif pt1[1] == pt2[1]:
            if pt1[0] > pt2[0]:
                pt1, pt2 = pt2, pt1
            for i in range(pt1[0] + 1, pt2[0]):
                if self.grid[i][pt1[1]] != -1:
                    return False
            return True
        else:
            return False

    def check_2(self, screen, pt1, pt2, dr):
        pt3 = (pt1[0], pt2[1])
        if self.grid[pt3[0]][pt3[1]] == -1 and self.check_1(pt1, pt3) and self.check_1(pt3, pt2):
            if dr == True:
                # pygame.draw.line(screen, RED, self.cods[pt1[0]][pt1[1]], self.cods[pt3[0]][pt3[1]], 5)
                # pygame.draw.line(screen, RED, self.cods[pt2[0]][pt2[1]], self.cods[pt3[0]][pt3[1]], 5)
                return [(pt1, pt3), (pt3, pt2)]
            return True
        pt3 = (pt2[0], pt1[1])
        if self.grid[pt3[0]][pt3[1]] == -1 and self.check_1(pt1, pt3) and self.check_1(pt3, pt2):
            if dr == True:
                # pygame.draw.line(screen, RED, self.cods[pt1[0]][pt1[1]], self.cods[pt3[0]][pt3[1]], 5)
                # pygame.draw.line(screen, RED, self.cods[pt2[0]][pt2[1]], self.cods[pt3[0]][pt3[1]], 5)
                return [(pt1, pt3), (pt3, pt2)]
            return True
        return False

    def check_3(self, screen, pt1, pt2, dr):
        # case 1:
        if pt1[1] > pt2[1]:
            pt1, pt2 = pt2, pt1
        i = pt1[0] - 1
        while i >= 0:
            if self.grid[i][pt1[1]] != -1:
                break
            if self.check_2(screen, (i, pt1[1]), pt2, dr):
                if dr == True:
                    # pygame.draw.line(screen, RED, self.cods[pt1[0]][pt1[1]], self.cods[i][pt1[1]], 5)
                    rs = self.check_2(screen, (i, pt1[1]), pt2, True)
                    rs.append((pt1, (i, pt1[1])))
                    return rs
                return True
            i -= 1
        # case 2:
        i = pt1[0] + 1
        while i <= self.ROW + 1:
            if self.grid[i][pt1[1]] != -1:
                break
            if self.check_2(screen, (i, pt1[1]), pt2, dr):
                if dr == True:
                    rs = self.check_2(screen, (i, pt1[1]), pt2, True)
                    rs.append((pt1, (i, pt1[1])))
                    return rs
                    # pygame.draw.line(screen, RED, self.cods[pt1[0]][pt1[1]], self.cods[i][pt1[1]], 5)
                return True
            i += 1
        # case 3:
        i = pt1[1] - 1
        while i >= 0:
            if self.grid[pt1[0]][i] != -1:
                break
            if self.check_2(screen, (pt1[0], i), pt2, dr):
                if dr == True:
                    # pygame.draw.line(screen, RED, self.cods[pt1[0]][pt1[1]], self.cods[pt1[0]][i], 5)
                    rs = self.check_2(screen, (pt1[0], i), pt2, True)
                    rs.append((pt1, (pt1[0], i)))
                    return rs
                return True
            i -= 1
        # case 4:
        i = pt1[1] + 1
        while i <= self.COL + 1:
            if self.grid[pt1[0]][i] != -1:
                break
            if self.check_2(screen, (pt1[0], i), pt2, dr):
                if dr == True:
                    # pygame.draw.line(screen, RED, self.cods[pt1[0]][pt1[1]], self.cods[pt1[0]][i], 5)
                    rs = self.check_2(screen, (pt1[0], i), pt2, True)
                    rs.append((pt1, (pt1[0], i)))
                    return rs
                return True
            i += 1
        return False
        
    def is_valid(self, screen, pt1, pt2, dr):
        if self.check_1(pt1, pt2):
            # draw line
            if dr == True:
                # pygame.draw.line(screen, RED, self.cods[pt1[0]][pt1[1]], self.cods[pt2[0]][pt2[1]], 5)
                return [(pt1, pt2)]
            return True
        elif self.check_2(screen, pt1, pt2, dr):
            return self.check_2(screen, pt1, pt2, dr)
        elif self.check_3(screen, pt1, pt2, dr):
            return self.check_3(screen, pt1, pt2, dr)
        else:
            return False
    def is_impossible(self, screen):
        for i in range(self.ROW):
            for j in range(self.COL):
                for ii in range(self.ROW):
                    for jj in range(self.COL):
                        if i == ii and j == jj:
                            continue
                        if self.grid[i + 1][j + 1] != -1 and self.grid[i + 1][j + 1] == self.grid[ii + 1][jj + 1] and self.is_valid(screen, (i + 1, j + 1), (ii + 1, jj + 1), False):
                            return (i + 1, j + 1), (ii + 1, jj + 1)
        return -1
    
    def suffle(self):
        a = []
        for i in range(self.ROW):
            for j in range(self.COL):
                if self.grid[i + 1][j + 1] != -1:
                    a.append(self.grid[i + 1][j + 1])
                    self.grid[i + 1][j + 1] = 0
        random.shuffle(a)
        ind = 0
        for i in range(self.ROW):
            for j in range(self.COL):
                if self.grid[i + 1][j + 1] == 0:
                    self.grid[i + 1][j + 1] = a[ind]
                    ind += 1
                    
    def is_winning(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COL + 1):
                if self.grid[i][j] != -1:
                    return False
        return True
    
    def game(self, screen):
        pre_hint1, pre_hint2 = -1, -1
        last = None
        drawing = False
        draw_counter = 0
        lines = []
        NUM_SNOWFLAKES = 200
        snowflakes = []
        for _ in range(NUM_SNOWFLAKES):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(2, 5)
            speed = random.uniform(1, 3)
            snowflakes.append({"x": x, "y": y, "size": size, "speed": speed})
        clock = pygame.time.Clock()
        
        while True:
            # Lấp đầy cửa sổ với màu trắng
            screen.blit(background_img, (0, 0))

            for snowflake in snowflakes:
                pygame.draw.circle(screen, WHITE, (int(snowflake["x"]), int(snowflake["y"])), snowflake["size"])
                snowflake["y"] += snowflake["speed"]
                if snowflake["y"] > height:
                    snowflake["y"] = random.randint(-20, -5)
                    snowflake["x"] = random.randint(0, width)
            
            b_button = pygame.Rect(40, 50, 75, 65)
            h_button = pygame.Rect(1085, 50, 75, 65)
            if self.is_winning():
                return 1
            while self.is_impossible(screen) == -1:
                print('Impossible')
                self.suffle()
            # vẽ bàn pikachu
            hint1, hint2 = self.is_impossible(screen)
            if hint1 != pre_hint1 and hint2 != pre_hint2:
                print('Hint :', hint1, hint2)
                pre_hint1, pre_hint2 = hint1, hint2
            x = (700 - self.ROW * IMAGE_SIZE[0]) // 2
            for i in range(self.ROW):
                y = (1200 - self.COL * IMAGE_SIZE[1]) // 2
                for j in range(self.COL):
                    if self.grid[i + 1][j + 1] != -1:
                        img = pygame.image.load(path[self.grid[i + 1][j + 1]])
                        screen.blit(img, (y, x))
                        if last == (i + 1, j + 1):
                            shadow_offset = 5  # Dịch chuyển để tạo hiệu ứng đậm
                            screen.blit(img, (y + shadow_offset, x + shadow_offset))
                    y += IMAGE_SIZE[1]
                x += IMAGE_SIZE[0]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Nếu người dùng đóng cửa sổ
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if b_button.collidepoint(event.pos):
                        return 'back'
                    elif h_button.collidepoint(event.pos):
                        lines = self.is_valid(screen, hint1, hint2, True)
                        drawing = True
                    # print('Mouse :', event.pos)
                    for i in range(self.ROW):
                        for j in range(self.COL):
                            if self.grid_button[i][j].collidepoint(event.pos):
                                if last is None:
                                    last = (i + 1, j + 1)
                                    # print('1 choose :', last)
                                else:
                                    if (i + 1, j + 1) == last:
                                        last = None
                                        break
                                    if self.grid[i + 1][j + 1] == self.grid[last[0]][last[1]]:
                                        # print('2 choose :', (i + 1, j + 1))
                                        if self.is_valid(screen, (i + 1, j + 1), last, True) != False:
                                            lines = self.is_valid(screen, (i + 1, j + 1), last, True)
                                            # print(lines)
                                            self.grid[i + 1][j + 1], self.grid[last[0]][last[1]] = -1, -1
                                            drawing = True
                                    last = None
            draw_button(screen, back_button, 40, 50)
            draw_button(screen, hint_button, 1085, 50)
            # Cập nhật cửa sổ
            if drawing == True:
                for l in lines:
                    pass
                    pygame.draw.line(screen, RED, self.cods[l[0][0]][l[0][1]], self.cods[l[1][0]][l[1][1]], 4)
                if draw_counter >= 20:
                    lines = []
                    draw_counter = 0
                    drawing = False
                else:
                    draw_counter += 1
            if self.is_winning():
                return 1
            clock.tick(60)
            pygame.display.flip()
    def show(self):
        for row in self.grid:
            print(row)
    
if __name__ == '__main__':
    grid = Grid(8, 6)
    grid.reset_grid()
    grid.show()