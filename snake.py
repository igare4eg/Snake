import pygame
import random
from os import path

# Размер окна
dis_width = 800
dis_height = 800
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Начало - основные характеристики окна + блоки для игры
pygame.init()
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
snake_block = 35
snake_step = 35
FPS = 9

music_dir = path.join(path.dirname(__file__), 'music')
img = pygame.image.load(path.join(music_dir, 'фон.jpg')).convert()
img = pygame.transform.scale(img, (dis_width, dis_height))
img_rect = img.get_rect()
img_1 = pygame.image.load(path.join(music_dir, 'game_over.jpg')).convert()
img_1 = pygame.transform.scale(img_1, (dis_width, dis_height))
img_1_rect = img_1.get_rect()
pygame.mixer.music.load(path.join(music_dir, 'friends.mp3'))
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)
am = pygame.mixer.Sound(path.join(music_dir, 'apple_bite.ogg'))
am.set_volume(0.2)


# Функция съедения
def eating_check(xcor, ycor, food_x, food_y):
    if food_x - snake_block <= xcor <= food_x + snake_block:
        if food_y - snake_block <= ycor <= food_y + snake_block:
            return True
    else:
        return False


# Создание текста в игре
def create_mes(msg, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size, bold=True)
    mes = font_style.render(msg, True, color)
    dis.blit(mes, [x, y])


def draw_head(i, snake_list):
    snake_head_img = head_img[i]
    snake_head = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
    snake_head.set_colorkey(BLACK)
    snake_head_rect = snake_head.get_rect(x=snake_list[-1][0], y=snake_list[-1][1])
    dis.blit(snake_head, snake_head_rect)


def draw_tail(i, snake_list):
    snake_tail_img = tail_img[i]
    snake_tail = pygame.transform.scale(snake_tail_img, (snake_block, snake_block))
    snake_tail.set_colorkey(WHITE)
    snake_tail_rect = snake_tail.get_rect(x=snake_list[0][0], y=snake_list[0][1])
    dis.blit(snake_tail, snake_tail_rect)

# def draw_body(i, snake_list):
#     for i, (x, y) in enumerate(snake_list[1:-1]):
#         prev_x, prev_y = snake_list[i]
#         next_x, next_y = snake_list[i + 2]
#         if prev_x == next_x:
#             if prev_y < next_y:
#                 img_name = 'body.png'
#             else:
#                 img_name = 'body.png'
#         else:
#             if prev_x < next_x:
#                 img_name = 'bodyDOWN.png'
#             else:
#                 img_name = 'bodyDOWN.png'
#         snake_body_img = pygame.image.load(path.join(music_dir, img_name)).convert()
#         snake_body = pygame.transform.scale(snake_body_img, (snake_block, snake_block))
#         snake_body.set_colorkey(WHITE)
#         snake_body_rect = snake_body.get_rect(x=x, y=y)
#         dis.blit(snake_body, snake_body_rect)



food_img = [
    pygame.image.load(path.join(music_dir, "banana.png")).convert(),
    pygame.image.load(path.join(music_dir, "green-apple.png")).convert(),
    pygame.image.load(path.join(music_dir, "red-cherry.png")).convert(),
    pygame.image.load(path.join(music_dir, "red-grape.png")).convert(),
    pygame.image.load(path.join(music_dir, "strawberry.png")).convert(),
    pygame.image.load(path.join(music_dir, "watermelon.png")).convert()
]
head_img = [
    pygame.image.load(path.join(music_dir, "headL.png")).convert(),
    pygame.image.load(path.join(music_dir, "headR.png")).convert(),
    pygame.image.load(path.join(music_dir, "headT.png")).convert(),
    pygame.image.load(path.join(music_dir, "headB.png")).convert()
]
tail_img = [
    pygame.image.load(path.join(music_dir, "tailLEFT.png")).convert(),
    pygame.image.load(path.join(music_dir, "tailRIGHT.png")).convert(),
    pygame.image.load(path.join(music_dir, "tailUP.png")).convert(),
    pygame.image.load(path.join(music_dir, "tailDOWN.png")).convert()
]


# Движок игры
def gameloop():
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    length = 2
    snake_list = []
    i = 0

    food_x = random.randrange(0, dis_width - snake_block)
    food_y = random.randrange(0, dis_height - snake_block)
    food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
    food.set_colorkey(WHITE)
    food_rect = food.get_rect(x=food_x, y=food_y)

    game_close = False
    run = True
    while run:
        while game_close:
            dis.fill(BLACK)
            # dis.blit(img_1, img_1_rect)
            create_mes('''Press Q for exit''', WHITE, 170, 100, "PressStart2P-Regular", 30)
            create_mes('''Press C for repeat game''', WHITE, 60, 200, "PressStart2P-Regular", 30)
            create_mes('''GAME OVER''', RED, 190, 350, "PressStart2P-Regular", 50)
            create_mes(f'Finally score: {length - 2}', WHITE, 130, 550, 'PressStart2P-Regular', 35)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_close = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        game_close = False
                    if event.key == pygame.K_c:
                        gameloop()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_step
                    y1_change = 0
                    i = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_step
                    y1_change = 0
                    i = 1
                elif event.key == pygame.K_UP:
                    y1_change = -snake_step
                    x1_change = 0
                    i = 2
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_step
                    x1_change = 0
                    i = 3
            elif event.type == pygame.QUIT:
                run = False
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(BLUE)
        dis.blit(img, img_rect)
        # отрисовка еды
        # pygame.draw.rect(dis, GREEN, [food_x, food_y, snake_block, snake_block])
        dis.blit(food, food_rect)
        # параметры змеи

        # отрисовка змеи
        for x in snake_list[1:]:
            # pygame.draw.rect(dis, BLACK, [x[0], x[1], snake_block, snake_block])
            snake = pygame.image.load(path.join(music_dir, 'body3.png')).convert()
            snake = pygame.transform.scale(snake, (snake_block, snake_block))
            snake.set_colorkey(WHITE)
            dis.blit(snake, (x[0], x[1]))
        snake_head = [x1, y1]
        # snake_head.append(x1)
        # snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]

        create_mes(f'Score: {length - 2}', GREEN, 10, 10, 'PressStart2P-Regular', 30)
        pygame.display.update()

        # Если змейка врезалась в себя
        for x in snake_list[1:-1]:
            if x == snake_head:
                game_close = True

        draw_head(i, snake_list)
        # for j in range(len(snake_list) -1, 0, -1):
        #     draw_body(i, snake_list)
        if length > 2:
            draw_tail(i, snake_list)

        if eating_check(x1, y1, food_x, food_y):
            food_x = random.randrange(0, dis_width - snake_block)
            food_y = random.randrange(0, dis_height - snake_block)
            food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
            food.set_colorkey(WHITE)
            food_rect = food.get_rect(x=food_x, y=food_y)
            length += 1
            am.play()

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    quit()


# Запуск
gameloop()
