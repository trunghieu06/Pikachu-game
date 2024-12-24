import pygame
import random
import sys
import os
import glob
import math
import json
from grid import *


path = [i.replace('\\', '/') for i in glob.glob('./DataSet/*.png')]

class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.Grid = None

player_data = dict()

with open('player.json', 'r') as f:
    player_data = json.load(f)
    
NO_PLAYER = len(player_data)
print(NO_PLAYER)
players = []
for k in player_data.keys():
    i = player_data[k]
    grid = Grid(int(i["Grid"]["row"]), int(i["Grid"]["col"]))
    grid.set_grid(i["Grid"]["grid"])
    temp = Player(k, i["password"])
    temp.Grid = grid
    players.append(temp)
    
def save_data():
    for i in player_data.keys():
        for j in players:
            if i == j.username:
                player_data[i]["Grid"]["grid"] = j.Grid.grid
                player_data[i]["Grid"]["row"] = j.Grid.ROW
                player_data[i]["Grid"]["col"] = j.Grid.COL
    for j in players:
        if j.username not in player_data.keys():
            player_data[j.username] = dict()
            player_data[j.username]["password"] = j.password
            player_data[j.username]["Grid"] = dict()
            player_data[j.username]["Grid"]["grid"] = j.Grid.grid
            player_data[j.username]["Grid"]["row"] = j.Grid.ROW
            player_data[j.username]["Grid"]["col"] = j.Grid.COL
    with open('player.json', 'w') as f:
        json.dump(player_data, f, indent=4)
    
def check_login(username, password):
    username = username.strip()
    password = password.strip()
    for i in players:
        if i.username == username and i.password == password:
            print('Login success')
            return players.index(i)
    print('Login failed')
    return None

pygame.init()

width, height = 1200, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Pikachu")  
font = pygame.font.Font("Tiny5-Regular.ttf", 60)
font_med = pygame.font.Font("Tiny5-Regular.ttf", 45)
font_mini = pygame.font.Font("Tiny5-Regular.ttf", 32)
button_img = pygame.image.load('button.png')
typing_box = pygame.image.load('typing_box.png')
back_button = pygame.image.load('back_button.png')
  

NUM_SNOWFLAKES = 200

snowflakes = []
for _ in range(NUM_SNOWFLAKES):
    x = random.randint(0, width)
    y = random.randint(0, height)
    size = random.randint(2, 5)
    speed = random.uniform(1, 3)
    snowflakes.append({"x": x, "y": y, "size": size, "speed": speed})

def draw(screen, font, text, color, x, y):
    text = font.render(text, True, color)
    text_rect = text.get_rect(center = (x, y))
    screen.blit(text, text_rect)

def draw_text(screen, font, text, color, x, y):
    text = font.render(text, True, color)
    screen.blit(text, (x, y))
    
def draw_button(screen, img, x, y):
    screen.blit(img, (x, y))
    
clock = pygame.time.Clock()


def winning_screen(screen):
    running = True
    while running:
        screen.blit(background_img, (0, 0))
        
        for snowflake in snowflakes:
            pygame.draw.circle(screen, WHITE, (int(snowflake["x"]), int(snowflake["y"])), snowflake["size"])
            snowflake["y"] += snowflake["speed"]
            if snowflake["y"] > height:
                snowflake["y"] = random.randint(-20, -5)
                snowflake["x"] = random.randint(0, width)
                
        draw(screen, font, 'You win', GREEN, width // 2, 200)
        
        draw_button(screen, button_img, 444, 300)
        draw(screen, font_med, 'Play again', BLACK, 600, 337)
        p_button = pygame.Rect(440, 300, 313, 84)
        draw_button(screen, button_img, 444, 450)
        draw(screen, font_med, 'Back', BLACK, 600, 487)
        b_button = pygame.Rect(440, 450, 313, 84)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_button.collidepoint(event.pos):
                    print('Back')
                    return 'back'
                elif p_button.collidepoint(event.pos):
                    print('Play again')
                    return 'play again'
        clock.tick(60)
        pygame.display.flip()
    save_data()
    pygame.quit()
    sys.exit()

def choose_size(screen):
    running = True
    row, col = 4, 4
    while running:
        screen.blit(background_img, (0, 0))
        
        for snowflake in snowflakes:
            pygame.draw.circle(screen, WHITE, (int(snowflake["x"]), int(snowflake["y"])), snowflake["size"])
            snowflake["y"] += snowflake["speed"]
            if snowflake["y"] > height:
                snowflake["y"] = random.randint(-20, -5)
                snowflake["x"] = random.randint(0, width)
                
        draw(screen, font, 'Choose Grid Size', GREEN, width // 2, 200)
        
        draw(screen, font_med, f'Rows: {row}', YELLOW, width // 2, 300)
        draw(screen, font_med, f'Cols: {col}', YELLOW, width // 2, 400)
        
        draw_button(screen, button_img, 444, 500)
        draw(screen, font_med, 'Confirm', BLACK, 600, 537)
        c_button = pygame.Rect(440, 500, 313, 84)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if c_button.collidepoint(event.pos):
                    return row, col
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    row += 2
                elif event.key == pygame.K_DOWN:
                    row -= 2
                elif event.key == pygame.K_RIGHT:
                    col += 2
                elif event.key == pygame.K_LEFT:
                    col -= 2
        
        row = max(2, min(row, 12))
        col = max(2, min(col, 24))
        
        clock.tick(60)
        pygame.display.flip()
    save_data()
    pygame.quit()
    sys.exit()
    
def login_func(screen):
    running = True
    u_text, p_text = '', ''
    status = 'username'
    mess = ''
    mess_counter = 0
    while running:
        screen.blit(background_img, (0, 0))
        
        for snowflake in snowflakes:
            pygame.draw.circle(screen, WHITE, (int(snowflake["x"]), int(snowflake["y"])), snowflake["size"])
            snowflake["y"] += snowflake["speed"]
            if snowflake["y"] > height:
                snowflake["y"] = random.randint(-20, -5)
                snowflake["x"] = random.randint(0, width)
                
        draw(screen, font, 'Username', GREEN, width // 2, 200)
        draw_button(screen, typing_box, 350, 230)
        u_button = pygame.Rect(350, 230, 500, 84)
        draw(screen, font, 'Password', GREEN, width // 2, 350)
        draw_button(screen, typing_box, 350, 380)
        p_button = pygame.Rect(350, 380, 500, 84)
        draw_button(screen, button_img, 444, 500)
        draw(screen, font_med, 'Login', BLACK, 600, 537)
        l_button = pygame.Rect(440, 500, 313, 84)
        draw_button(screen, back_button, 50, 50)
        b_button = pygame.Rect(50, 50, 75, 65)
        draw_text(screen, font_mini, u_text, BLACK, 375, 253)
        draw_text(screen, font_mini, p_text, BLACK, 375, 403)   
        
        if mess != '' and mess_counter < 20:
            draw(screen, font_mini, mess, RED, 600, 603)
            mess_counter += 1
        else:
            mess = ''
            mess_counter = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if u_button.collidepoint(event.pos):
                    print('Username')
                    status = 'username' 
                    # nhap username
                    pass
                elif p_button.collidepoint(event.pos):
                    # nhap password
                    print('Password')
                    status = 'password'
                    pass
                elif l_button.collidepoint(event.pos):
                    # login
                    if u_text == '':
                        draw(screen, font_mini, 'Enter username', RED, 600, 603)
                        mess = 'Enter username'
                        mess_counter = 0
                    elif p_text == '':
                        draw(screen, font_mini, 'Enter password', RED, 600, 603)
                        mess = 'Enter password'
                        mess_counter = 0
                    else:
                        temp = check_login(u_text, p_text)
                        if temp == None:
                            draw(screen, font_mini, 'Login failed', RED, 600, 603)
                            mess = 'Login failed'
                            mess_counter = 0
                        else:
                            print('Login success')
                            return temp
                    print('Login')  
                    pass    
                elif b_button.collidepoint(event.pos):
                    print('Back')
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if status == 'username':
                        u_text = u_text[:-1]
                    else:
                        p_text = p_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if status == 'username':
                        print('Username:', u_text)
                        status = 'password'
                    else:
                        print('Password:', p_text)
                        # check login
                        temp = check_login(u_text, p_text)
                        if temp == None:
                            draw(screen, font_mini, 'Login failed', RED, 600, 603)
                            mess = 'Login failed'
                            mess_counter = 0
                        else:
                            print('Login success')
                            return temp
                else:
                    if status == 'username':
                        u_text += event.unicode
                    else:
                        p_text += event.unicode
        if status == 'username':
            draw_text(screen, font_mini, u_text, BLACK, 375, 253)
            if pygame.time.get_ticks() % 1000 < 500:
                draw_text(screen, font_mini, '|', BLACK, 375 + font_mini.size(u_text)[0], 253)
        elif status == 'password':
            draw_text(screen, font_mini, p_text, BLACK, 375, 403)
            if pygame.time.get_ticks() % 1000 < 500:
                draw_text(screen, font_mini, '|', BLACK, 375 + font_mini.size(p_text)[0], 403)
        
        clock.tick(60)
        pygame.display.flip()
    save_data()
    pygame.quit()
    sys.exit()
    
def guest_func(screen):
    row, col = choose_size(screen)
    guest = Grid(row, col)
    guest.reset_grid()
    running = True
    while running:
        screen.blit(background_img, (0, 0))
        
        for snowflake in snowflakes:
            pygame.draw.circle(screen, WHITE, (int(snowflake["x"]), int(snowflake["y"])), snowflake["size"])
            snowflake["y"] += snowflake["speed"]
            if snowflake["y"] > height:
                snowflake["y"] = random.randint(-20, -5)
                snowflake["x"] = random.randint(0, width)
                
        gm = guest.game(screen)
        
        if gm == 1:
            opt = winning_screen(screen)
            if opt == 'back':
                return
            else:
                newr, newc = choose_size(screen)
                guest = Grid(newr, newc)
                guest.reset_grid()
        elif gm == False:
            running = False
        elif gm == 'back':
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
    sys.exit()
    
def signup_func(screen):
    running = True
    u_text, p_text, r_text = '', '', ''
    status = 'username'
    mess = ''
    mess_counter = 0
    while running:
        screen.blit(background_img, (0, 0))
        
        for snowflake in snowflakes:
            pygame.draw.circle(screen, WHITE, (int(snowflake["x"]), int(snowflake["y"])), snowflake["size"])
            snowflake["y"] += snowflake["speed"]
            if snowflake["y"] > height:
                snowflake["y"] = random.randint(-20, -5)
                snowflake["x"] = random.randint(0, width)
                
        draw(screen, font, 'Username', GREEN, width // 2, 100)
        draw_button(screen, typing_box, 350, 130)
        u_button = pygame.Rect(350, 130, 500, 84)
        
        draw(screen, font, 'Password', GREEN, width // 2, 250)
        draw_button(screen, typing_box, 350, 280)
        p_button = pygame.Rect(350, 280, 500, 84)
        
        draw(screen, font, 'Repassword', GREEN, width // 2, 400)
        draw_button(screen, typing_box, 350, 430)
        r_button = pygame.Rect(350, 430, 500, 84)
        
        draw_button(screen, back_button, 50, 50)
        b_button = pygame.Rect(50, 50, 75, 65)
        
        draw_button(screen, button_img, 444, 550)
        draw(screen, font_med, 'Sign up', BLACK, 600, 587)
        s_button = pygame.Rect(440, 550, 313, 84)
        
        draw_text(screen, font_mini, u_text, BLACK, 375, 153)
        draw_text(screen, font_mini, p_text, BLACK, 375, 303)   
        draw_text(screen, font_mini, r_text, BLACK, 375, 453)
        
        if mess != '' and mess_counter < 20:
            draw(screen, font_mini, mess, RED, 600, 603)
            mess_counter += 1
        else:
            mess = ''
            mess_counter = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if u_button.collidepoint(event.pos):
                    print('Username')
                    status = 'username' 
                elif p_button.collidepoint(event.pos):
                    print('Password')
                    status = 'password'
                elif r_button.collidepoint(event.pos):
                    print('Repassword')
                    status = 'repassword'
                elif b_button.collidepoint(event.pos):
                    print('Back')
                    return
                elif s_button.collidepoint(event.pos):
                    if u_text == '':
                        mess = 'Enter username'
                        mess_counter = 0
                    elif p_text == '':
                        mess = 'Enter password'
                        mess_counter = 0
                    elif r_text == '':
                        mess = 'Enter repassword'
                        mess_counter = 0
                    elif p_text != r_text:
                        draw(screen, font_mini, 'Password not match', RED, 600, 603)
                        mess = 'Password not match'
                        mess_counter = 0
                    else:
                        print('Signup success')
                        temp = Player(u_text, p_text)
                        temp.Grid = Grid(4, 4)
                        players.append(temp)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if status == 'username':
                        u_text = u_text[:-1]
                    elif status == 'password':
                        p_text = p_text[:-1]
                    elif status == 'repassword':
                        r_text = r_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if status == 'username':
                        print('Username:', u_text)
                        status = 'password'
                    elif status == 'password':
                        print('Password:', p_text)
                        status = 'repassword'
                    else:
                        print('Repassword:', r_text)
                        if p_text != r_text:
                            mess = 'Password not match'
                            mess_counter = 0
                        else:
                            print('Signup success')
                            temp = Player(u_text, p_text)
                            temp.Grid = Grid(4, 4)
                            players.append(temp)
                            return
                else:
                    if status == 'username':
                        u_text += event.unicode
                    elif status == 'password':
                        p_text += event.unicode
                    elif status == 'repassword':
                        r_text += event.unicode
        if status == 'username':
            if pygame.time.get_ticks() % 1000 < 500:
                draw_text(screen, font_mini, '|', BLACK, 375 + font_mini.size(u_text)[0], 153)
        elif status == 'password':
            if pygame.time.get_ticks() % 1000 < 500:
                draw_text(screen, font_mini, '|', BLACK, 375 + font_mini.size(p_text)[0], 303)
        elif status == 'repassword':
            if pygame.time.get_ticks() % 1000 < 500:
                draw_text(screen, font_mini, '|', BLACK, 375 + font_mini.size(r_text)[0], 453)
        
        clock.tick(60)
        pygame.display.flip()
    save_data()
    pygame.quit()
    sys.exit()
    
id = None
running = True
while running:
    screen.blit(background_img, (0, 0))
    
    # title
    draw(screen, font, 'Pikachu Game', YELLOW, width // 2, 100)
    draw(screen, font_mini, 'by S.I.C.K', YELLOW, 800, 150)
    
    for snowflake in snowflakes:
        pygame.draw.circle(screen, WHITE, (int(snowflake["x"]), int(snowflake["y"])), snowflake["size"])
        snowflake["y"] += snowflake["speed"] 
        if snowflake["y"] > height:
            snowflake["y"] = random.randint(-20, -5) 
            snowflake["x"] = random.randint(0, width)
    
    if id is not None:
        gm = players[id].Grid.game(screen)
        if gm == 1:
            opt = winning_screen(screen)
            if opt == 'back':
                id = None
                continue
            else:
                newr, newc = choose_size(screen)
                players[id].Grid = Grid(newr, newc)
                players[id].Grid.reset_grid()
        elif gm == False:
            running = False
        elif gm == 'back':
            save_data()
            id = None
    else:
        draw_button(screen, button_img, 444, 250)
        draw_button(screen, button_img, 444, 400)
        draw_button(screen, button_img, 444, 550)
        button1 = pygame.Rect(440, 250, 313, 84)
        button2 = pygame.Rect(440, 400, 313, 84)
        button3 = pygame.Rect(440, 550, 313, 84)
        draw(screen, font_med, 'Login', BLACK, 600, 287)
        draw(screen, font_med, 'Play as guest', BLACK, 600, 437)
        draw(screen, font_med, 'Sign up', BLACK, 600, 587)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(event.pos):
                    id = login_func(screen)
                    print('PlayerID:', id)
                elif button2.collidepoint(event.pos):
                    guest_func(screen)
                elif button3.collidepoint(event.pos):
                    id = len(players)
                    signup_func(screen)
                    r, c = choose_size(screen)
                    players[id].Grid = Grid(r, c)
                    players[id].Grid.reset_grid()
                    players[id].Grid.ROW = r
                    players[id].Grid.COL = c
                
    pygame.display.flip()
    clock.tick(60)



# Thoát khỏi Pygame
save_data()
pygame.quit()
sys.exit()