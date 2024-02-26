import os
import random
import sys
import pygame
from sys import stdin


pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 60
WIDTH = 400
HEIGHT = 300
STEP = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


# Функция загрузки изображения
def load_image(name, transparent=False):
    fullname = os.path.join('resources', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if transparent:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


# Функция загрузки уровня
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину    
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')    
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# Генерация уровня на основе загруженной карты
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках            
    return new_player, x, y, level


# Функция закрытия приложения
def terminate():
    pygame.quit()
    sys.exit()


# Стартовое окно
def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 30)
    text_coord = 50
    text_out = []
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        text_out.append((string_rendered, intro_rect))
    # Отрисовка
    while True:
        screen.blit(fon, (0, 0))
        fps = str(random.randint(2, 70))
        string_rendered = font.render(fps, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 50
        intro_rect.x = WIDTH - 50
        screen.blit(string_rendered, intro_rect)

        for i in text_out:
            screen.blit(i[0], i[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# Реестр изображений
tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png', transparent=True)
# Размер блоков
tile_width = tile_height = 50


# Класс блока/плитки
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


# Класс персонажа
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


# Запуск сначала стартового окна
start_screen()

# Загрузка и генерация уровня
level_name = stdin.read()
player, level_x, level_y, level = generate_level(load_level(level_name.strip()))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            num_row = player.rect.y // 50
            num_col = player.rect.x // 50
            if event.key == pygame.K_LEFT and level[num_row][num_col - 1] in ['.', '@']:
                player.rect.x -= STEP
            if event.key == pygame.K_RIGHT and level[num_row][num_col + 1] in ['.', '@']:
                player.rect.x += STEP
            if event.key == pygame.K_UP and level[num_row - 1][num_col] in ['.', '@']:
                player.rect.y -= STEP
            if event.key == pygame.K_DOWN and level[num_row + 1][num_col] in ['.', '@']:
                player.rect.y += STEP

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

# Выход из игры
terminate()
