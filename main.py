import pygame
import random
import sys
import os
import glob


path = [i.replace('\\', '/') for i in glob.glob('./DataSet/*.png')]

# Màu sắc (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

NO_IMAGE = len(path)

print(NO_IMAGE)

ROW, COL = 6, 5
grid = [[-1] * (COL + 3) for _ in range(ROW + 3)]
cods = [[-1] * (COL + 3) for _ in range(ROW + 3)]
ROW = min(ROW, 12)
COL = min(COL, 25)

err = []
cnt = 0

for i in range(1, ROW + 1):
    for j in range(1, COL + 1):
        left = ROW * COL - cnt
        if len(err) == left:
           ind = random.randint(0, len(err) - 1)
           grid[i][j] = err[ind]
           err.pop(ind)
        else:
           grid[i][j] = random.randint(0, NO_IMAGE - 1)
           if grid[i][j] not in err:
               err.append(grid[i][j])
           else:
               err.remove(grid[i][j])
        cnt += 1
        
# for row in grid:
#     for ele in row:
#         print(ele, end = ' ')
#     print()
        
# cnt = [0] * (NO_IMAGE)
# for row in grid:
#     for ele in row:
#         cnt[ele] += 1

pygame.init()

# Kích thước cửa sổ
width, height = 1200, 700
screen = pygame.display.set_mode((width, height))  # Tạo cửa sổ với kích thước (width, height)
pygame.display.set_caption("Game Pikachu")  # Đặt tiêu đề cho cửa sổ

IMAGE_SIZE = (50, 40)
grid_button = [[pygame.Rect(0, 0, 0, 0)] * (COL) for _ in range(ROW)]
x = (700 - ROW * IMAGE_SIZE[0]) // 2
for i in range(ROW):
    y = (1200 - COL * IMAGE_SIZE[1]) // 2
    for j in range(COL):
        grid_button[i][j] = pygame.Rect(y, x, IMAGE_SIZE[1], IMAGE_SIZE[0])
        cods[i + 1][j + 1] = (y + IMAGE_SIZE[1] // 2, x + IMAGE_SIZE[0] // 2)
        y += IMAGE_SIZE[1]
    x += IMAGE_SIZE[0]
for i in range(1, COL + 1):
    cods[0][i] = (cods[1][i][0], cods[1][i][1] - IMAGE_SIZE[0])
    cods[ROW + 1][i] = (cods[ROW][i][0], cods[ROW][i][1] + IMAGE_SIZE[0])
for i in range(1, ROW + 1):
    cods[i][0] = (cods[i][1][0] - IMAGE_SIZE[1], cods[i][1][1])
    cods[i][COL + 1] = (cods[i][COL][0] + IMAGE_SIZE[1], cods[i][COL][1])
last = None
drawing = False

def check_1(pt1, pt2):
    # 2 cases
    if pt1[0] == pt2[0]:
        if pt1[1] > pt2[1]:
            pt1, pt2 = pt2, pt1
        for i in range(pt1[1] + 1, pt2[1]):
            if grid[pt1[0]][i] != -1:
                return False
        return True
    elif pt1[1] == pt2[1]:
        if pt1[0] > pt2[0]:
            pt1, pt2 = pt2, pt1
        for i in range(pt1[0] + 1, pt2[0]):
            if grid[i][pt1[1]] != -1:
                return False
        return True
    else:
        return False

def check_2(pt1, pt2, dr):
    pt3 = (pt1[0], pt2[1])
    if grid[pt3[0]][pt3[1]] == -1 and check_1(pt1, pt3) and check_1(pt3, pt2):
        if dr == True:
            pygame.draw.line(screen, RED, cods[pt1[0]][pt1[1]], cods[pt3[0]][pt3[1]], 5)
            pygame.draw.line(screen, RED, cods[pt2[0]][pt2[1]], cods[pt3[0]][pt3[1]], 5)
        return True
    pt3 = (pt2[0], pt1[1])
    if grid[pt3[0]][pt3[1]] == -1 and check_1(pt1, pt3) and check_1(pt3, pt2):
        if dr == True:
            pygame.draw.line(screen, RED, cods[pt1[0]][pt1[1]], cods[pt3[0]][pt3[1]], 5)
            pygame.draw.line(screen, RED, cods[pt2[0]][pt2[1]], cods[pt3[0]][pt3[1]], 5)
        return True
    return False

def check_3(pt1, pt2, dr):
    # case 1:
    if pt1[1] > pt2[1]:
        pt1, pt2 = pt2, pt1
    i = pt1[0] - 1
    while i >= 0:
        if grid[i][pt1[1]] != -1:
            break
        if check_2((i, pt1[1]), pt2, dr):
            if dr == True:
                pygame.draw.line(screen, RED, cods[pt1[0]][pt1[1]], cods[i][pt1[1]], 5)
            return True
        i -= 1
    # case 2:
    i = pt1[0] + 1
    while i <= ROW + 1:
        if grid[i][pt1[1]] != -1:
            break
        if check_2((i, pt1[1]), pt2, dr):
            if dr == True:
                pygame.draw.line(screen, RED, cods[pt1[0]][pt1[1]], cods[i][pt1[1]], 5)
            return True
        i += 1
    # case 3:
    i = pt1[1] - 1
    while i >= 0:
        if grid[pt1[0]][i] != -1:
            break
        if check_2((pt1[0], i), pt2, dr):
            if dr == True:
                pygame.draw.line(screen, RED, cods[pt1[0]][pt1[1]], cods[pt1[0]][i], 5)
            return True
        i -= 1
    # case 4:
    i = pt1[1] + 1
    while i <= COL + 1:
        if grid[pt1[0]][i] != -1:
            break
        if check_2((pt1[0], i), pt2, dr):
            if dr == True:
                pygame.draw.line(screen, RED, cods[pt1[0]][pt1[1]], cods[pt1[0]][i], 5)
            return True
        i += 1
    return False
    
    
def is_valid(pt1, pt2, dr):
    if check_1(pt1, pt2):
        # draw line
        if dr == True:
            pygame.draw.line(screen, RED, cods[pt1[0]][pt1[1]], cods[pt2[0]][pt2[1]], 5)
        return True
    elif check_2(pt1, pt2, dr):
        return True
    elif check_3(pt1, pt2, dr):
        return True
    else:
        return False
    
def is_impossible():
    for i in range(ROW):
        for j in range(COL):
            for ii in range(ROW):
                for jj in range(COL):
                    if i == ii and j == jj:
                        continue
                    if grid[i + 1][j + 1] != -1 and grid[i + 1][j + 1] == grid[ii + 1][jj + 1] and is_valid((i + 1, j + 1), (ii + 1, jj + 1), False):
                        return (i + 1, j + 1), (ii + 1, jj + 1)
    return -1

def suffle():
    a = []
    for i in range(ROW):
        for j in range(COL):
            if grid[i + 1][j + 1] != -1:
                a.append(grid[i + 1][j + 1])
                grid[i + 1][j + 1] = 0
    random.shuffle(a)
    ind = 0
    for i in range(ROW):
        for j in range(COL):
            if grid[i + 1][j + 1] == 0:
                grid[i + 1][j + 1] = a[ind]
                ind += 1
    
def is_winning():
    for i in range(ROW):
        for j in range(COL):
            if grid[i][j] != -1:
                return False
    return True
    
pre_hint1, pre_hint2 = -1, -1
font = pygame.font.Font(None, 74)
text1 = font.render('No possible move', True, BLUE)
text2 = font.render('Resetting...', True, BLUE)
text_rect1 = text1.get_rect(center=(width // 2, height // 2))
text_rect2 = text2.get_rect(center=(width // 2, height // 2))

running = True
while running:
    # Lấp đầy cửa sổ với màu trắng
    screen.fill(WHITE)

    while is_impossible() == -1:
        print('Impossible')
        screen.blit(text1, text_rect1)
        pygame.display.flip()
        pygame.time.delay(500)
        screen.fill(WHITE)
        pygame.display.flip()
        screen.blit(text2, text_rect2)
        pygame.display.flip()
        pygame.time.delay(1000)
        screen.fill(WHITE)
        pygame.display.flip()
        suffle()
    # vẽ bàn pikachu
    hint1, hint2 = is_impossible()
    if hint1 != pre_hint1 and hint2 != pre_hint2:
        print('Hint :', hint1, hint2)
        pre_hint1, pre_hint2 = hint1, hint2
    x = (700 - ROW * IMAGE_SIZE[0]) // 2
    for i in range(ROW):
        y = (1200 - COL * IMAGE_SIZE[1]) // 2
        for j in range(COL):
            if grid[i + 1][j + 1] != -1:
                img = pygame.image.load(path[grid[i + 1][j + 1]])
                screen.blit(img, (y, x))
                if last == (i + 1, j + 1):
                    shadow_offset = 5  # Dịch chuyển để tạo hiệu ứng đậm
                    screen.blit(img, (y + shadow_offset, x + shadow_offset))
            y += IMAGE_SIZE[1]
        x += IMAGE_SIZE[0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Nếu người dùng đóng cửa sổ
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # print('Mouse :', event.pos)
            for i in range(ROW):
                for j in range(COL):
                    if grid_button[i][j].collidepoint(event.pos):
                        if last is None:
                            last = (i + 1, j + 1)
                            print('1 choose :', last)
                        else:
                            if (i + 1, j + 1) == last:
                                last = None
                                break
                            if grid[i + 1][j + 1] == grid[last[0]][last[1]]:
                                print('2 choose :', (i + 1, j + 1))
                                if is_valid((i + 1, j + 1), last, True):
                                    grid[i + 1][j + 1], grid[last[0]][last[1]] = -1, -1
                                    drawing = True
                            last = None

    # Cập nhật cửa sổ
    pygame.display.flip()
    if drawing == True:
        pygame.time.delay(500)
        drawing = False
    if is_winning():
        running = False

screen.fill(BLUE)
text = font.render('You Win!!', True, YELLOW)
text_rect = text.get_rect(center = (width // 2, height // 2))
screen.blit(text, text_rect)
pygame.display.flip()
paused = True
while paused:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            paused = False

# Thoát khỏi Pygame
pygame.quit()
sys.exit()