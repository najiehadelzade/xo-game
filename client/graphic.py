import pygame
import threading
import json

red = (255, 100, 100)

blue = (100, 100, 255)

yellow = (200,200,200)

green = (100, 255, 100)

gray = (128, 128, 128)

black = (0,0,0)

def init_graphic():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    screen.fill(gray)
    pygame.display.update()
    return screen

def display_board(screen, board):
    blocks = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(show_move(screen, i, j, board[i][j]))
        blocks.append(row)
    return blocks

def show_map(screen, board, color):
    screen.fill(color)

    pygame.draw.line(screen, black, (200, 0), (200, 600))
    pygame.draw.line(screen, black, (400, 0), (400, 600))
    pygame.draw.line(screen, black, (0, 400), (600, 400))
    pygame.draw.line(screen, black, (0, 200), (600, 200))

    blocks = display_board(screen, board)
    pygame.display.update()
    return blocks


def show_move(screen, i, j, m):
    
    y = i*200
    x = j*200
    if m == 1:
        img = pygame.image.load('client/x.png')
        return screen.blit(img,(x, y))
    elif m == 2:
        img = pygame.image.load('client/o.png')
        return screen.blit(img,(x, y))
    else:
        img = pygame.image.load('client/e.png')
        return screen.blit(img,(x, y))
    


def get_move(event, board, blocks):
    if event.type == pygame.MOUSEBUTTONDOWN:
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0 and blocks[i][j].collidepoint(event.pos):
                    return {'row':i, 'col':j}


def events(screen, client):
    running = True
    while True:
        if running:
            pygame.event.pump()
            pygame.time.delay(500)
        
            msg=client.socket.recv(1024).decode()
            if msg=='Wait for another player\n':
                pass
            else:
                dic=json.loads(msg)

                if dic['result']!=0:
                    running = False
                    client.stop()
                    if dic['result'] == 1:
                        show_map(screen, dic['board'], green)
                    else:
                        show_map(screen, dic['board'], red)

                elif dic['your_turn']==True:
                    pygame.event.pump()
                    while True:
                        blocks = show_map(screen, dic['board'], blue)
                        event = pygame.event.wait()
                        msg = get_move(event, dic['board'], blocks)
                        
                        if msg:
                            client.send(msg)
                            break
                else:
                    show_map(screen, dic['board'], yellow)
                    
        else:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                break
