import os
import sys
import pygame
import random

pygame.init()
clock = pygame.time.Clock()

size = width, height = 700, 500
screen = pygame.display.set_mode(size)
FPS = 50
STEP = 10
score = 0
player = pygame.sprite.Group()
fon = pygame.sprite.Group()
cls = pygame.sprite.Group()


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if name.endswith(".png"):
            image = image.convert_alpha()
        else:
            image = image.convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Игра Flappy Bird", "",
                  "Правила игры",
                  "Используйте Пробел, чтобы прыгать,",
                  "Пролетайте между колоннами и не врезайтесь!",
                  "Нажмите любую кнопку, чтобы начать."]

    fon = pygame.transform.scale(load_image('bckgrd.png'), (width * 3,
                                                            height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type ==  \
                    pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Fon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('bckgrd.png'), (width * 3,
                                                              height))
    speed = 1

    def __init__(self, group):
        super().__init__(group)
        self.image = Fon.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

    def update(self):
        self.rect.x -= Fon.speed
        if self.rect.x == -width * 2:
            self.rect.x = 0


class Bird(pygame.sprite.Sprite):
    speed = 2
    jump_flag = True
    up_flag = False
    dir_speed = 1

    def __init__(self, group, sheet, columns, rows, x, y):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.num = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.dir = 1
        self.k = 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.jump_flag:
            if self.rect.y + 50 < height:
                self.rect.y += Bird.speed
                if self.num == 12:
                    Bird.speed = 2
                self.num += 1
                self.k += 0.1
                self.cur_frame = (round(self.k)) % len(self.frames)
                self.image = self.frames[self.cur_frame]

    def jump(self):
        if Bird.jump_flag is True:
            Bird.up_flag = True
            Bird.speed = -5
            self.num = 0


class Column(pygame.sprite.Sprite):
    cl = load_image('cl.png')
    speed = 2

    def __init__(self, group):
        super().__init__(group)
        self.image = Column.cl
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width, -200 + random.randint(-179, 179)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.rect.x -= Column.speed
        if pygame.sprite.collide_mask(self, bird):
            Column.speed = 0
            Fon.speed = 0
            Bird.speed = 0
            Bird.jump_flag = False
            Bird.dir_speed = 0


bird = Bird(player, load_image("bird_sheet5x1.png"), 5, 1, width // 2,
            height // 2)
back = Fon(fon)
cl = Column(cls)
start_screen()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    screen.fill(pygame.Color('black'))
    if cl.rect.x < width / 2 - 130:
        cl = Column(cls)
        score += 1
    fon.update()
    fon.draw(screen)
    player.update()
    player.draw(screen)
    cls.update()
    cls.draw(screen)
    pygame.display.flip()
    clock.tick(75)

terminate()
