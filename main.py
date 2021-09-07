import pygame
import random
import os


class Point(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.value = 1
        self.image = point
        self.rect = self.image.get_rect()
        self.rect.center = [-100, 0]


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = wall
        self.rect = self.image.get_rect()
        self.rect.center = [-100, 0]


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.direction = [-1, 0]
        self.steps = 25
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.center = [-100, 0]

    def update(self):
        temp_rect = self.rect
        if self.steps > 0:
            self.steps -= 1
            temp_rect.x += self.direction[0]
            temp_rect.y += self.direction[1]
        else:
            if self.rect.center[0] % 25 != 0 or self.rect.center[1] % 25 != 0:
                print(self.rect.center)
            rnd = random.randint(0, 35)
            if rnd == 0:
                self.direction = [1, 0]
            elif rnd == 1:
                self.direction = [-1, 0]
            elif rnd == 2:
                self.direction = [0, 1]
            elif rnd == 3:
                self.direction = [0, -1]
            # print(self.rect.center)
            self.steps = 25
            # collision
            for wallStop in walls:
                if self.rect.x + self.direction[0]*25 < (wallStop.rect.x + wallStop.rect.w) \
                        and (self.rect.x + self.direction[0]*25 + self.rect.w) > wallStop.rect.x \
                        and self.rect.y + self.direction[1]*25 < (wallStop.rect.y + wallStop.rect.h) \
                        and (self.rect.h + self.rect.y + self.direction[1]*25) > wallStop.rect.y:
                    self.direction = [0, 0]
                    # print(self.rect.center)

            if temp_rect.left > WIDTH and self.direction[0] == 1:
                temp_rect.x = -24 + WIDTH - temp_rect.x
            elif temp_rect.right < 0 and self.direction[0] == -1:
                temp_rect.x = WIDTH + 1 - temp_rect.x
            elif temp_rect.bottom < 0 and self.direction[1] == -1:
                temp_rect.y = HEIGHT + 1 - temp_rect.y
            elif temp_rect.top > HEIGHT and self.direction[1] == 1:
                temp_rect.y = -24 + HEIGHT - temp_rect.y
            # move
            self.rect = temp_rect


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.points_count = 0
        self.image = player_img
        self.iter = 0
        self.rect = self.image.get_rect()
        self.rect.center = [50, 450]
        self.sprites = (run1img, player_img, run2img)
        # self.size = self.image.get_size()
        # self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.1), int(self.size[1]*0.1)))
        self.direction = [1, 0]
        self.oldDirection = [1, 0]
        self.steps = 25

    def update(self):
        # death
        enemy_hit = pygame.sprite.spritecollide(self, EnemySprs, False)
        if enemy_hit:
            global state
            state = 1
        # points
        points_hit = pygame.sprite.spritecollide(self, PointsSprs, True)
        if points_hit:
            for el in points_hit:
                self.points_count += el.value
            # print(self.points_count)
        # temp
        temp_rect = self.rect

        if self.steps > 0:
            self.steps -= 1
            temp_rect.x += self.oldDirection[0]
            temp_rect.y += self.oldDirection[1]
        else:
            # print(self.rect.center)
            self.steps = 25
            # collision
            self.oldDirection = self.direction
            for wallStop in walls:
                if self.rect.x + self.oldDirection[0]*25 < (wallStop.rect.x + wallStop.rect.w) \
                        and (self.rect.x + self.oldDirection[0]*25 + self.rect.w) > wallStop.rect.x \
                        and self.rect.y + self.oldDirection[1]*25 < (wallStop.rect.y + wallStop.rect.h) \
                        and (self.rect.h + self.rect.y + self.oldDirection[1]*25) > wallStop.rect.y:
                    self.oldDirection = [0, 0]
                    # print(self.rect.center)
        # anim
        self.image = self.sprites[round(self.iter / 30)]
        if self.iter > 30 * 2 or (self.oldDirection[0] == 0 and self.oldDirection[1] == 0):
            self.iter = 0
        else:
            self.iter += 1
        if self.direction[0] < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        # borders
        if temp_rect.left > WIDTH and self.oldDirection[0] == 1:
            temp_rect.x = -24
        elif temp_rect.right < 0 and self.oldDirection[0] == -1:
            temp_rect.x = WIDTH-1
        elif temp_rect.bottom < 0 and self.oldDirection[1] == -1:
            temp_rect.y = HEIGHT-1
        elif temp_rect.top > HEIGHT and self.oldDirection[1] == 1:
            temp_rect.y = -24
        # move
        self.rect = temp_rect


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 500
HEIGHT = 600
FPS = 120
#
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Student-Man")
clock = pygame.time.Clock()
#
game_folder = os.path.dirname(__file__)
data_folder = os.path.join(game_folder, 'data')
player_img = pygame.image.load(os.path.join(data_folder, 'idle.png')).convert()
player_img.set_colorkey(BLACK)
run1img = pygame.image.load(os.path.join(data_folder, 'run-1.png')).convert()
run1img.set_colorkey(BLACK)
run2img = pygame.image.load(os.path.join(data_folder, 'run-2.png')).convert()
run2img.set_colorkey(BLACK)
wall = pygame.image.load(os.path.join(data_folder, 'wall.png')).convert()
enemy = pygame.image.load(os.path.join(data_folder, 'enemy.png')).convert()
enemy.set_colorkey(BLACK)
point = pygame.image.load(os.path.join(data_folder, 'point.png')).convert()
point.set_colorkey(BLACK)
two_points = pygame.image.load(os.path.join(data_folder, 'two_points.png')).convert()
two_points.set_colorkey(BLACK)
down_bar = pygame.image.load(os.path.join(data_folder, 'bar.png')).convert()
fail = pygame.image.load(os.path.join(data_folder, 'fail.png')).convert()
win = pygame.image.load(os.path.join(data_folder, 'win.png')).convert()
icon = pygame.image.load(os.path.join(data_folder, 'icon.png')).convert()
pygame.display.set_icon(icon)
font = pygame.font.SysFont('Comic Sans MS', 30)

WallsSprs = pygame.sprite.Group()
PlayerSprs = pygame.sprite.Group()
EnemySprs = pygame.sprite.Group()
PointsSprs = pygame.sprite.Group()
player = Player()
PlayerSprs.add(player)
#
walls = []
enemies = []
points = []


def load():
    walls.clear()
    enemies.clear()
    points.clear()
    WallsSprs.empty()
    EnemySprs.empty()
    PointsSprs.empty()

    player.__init__()
    # points
    for i in range(0, 80):
        points.append(Point())
        points[len(points) - 1].rect.center = [random.randint(2, 18) * 25, random.randint(2, 18) * 25]
        if i >= 60:
            points[len(points) - 1].value = 2
            points[len(points) - 1].image = two_points

    # enemies
    enemies.append(Enemy())
    enemies[len(enemies) - 1].rect.center = [50, 250]
    enemies.append(Enemy())
    enemies[len(enemies) - 1].rect.center = [300, 425]

    # walls
    for i in range(0, 10):
        walls.append(Wall())
        walls[len(walls) - 1].rect.center = [0, 500 - i * 25]
    for i in range(0, 10):
        walls.append(Wall())
        walls[len(walls) - 1].rect.center = [0, 0 + i * 25]
    for i in range(0, 10):
        walls.append(Wall())
        walls[len(walls) - 1].rect.center = [500, 500 - i * 25]
    for i in range(0, 10):
        walls.append(Wall())
        walls[len(walls) - 1].rect.center = [500, 0 + i * 25]
    for i in range(1, 20):
        walls.append(Wall())
        walls[len(walls) - 1].rect.center = [0 + i * 25, 0]
    for i in range(1, 20):
        walls.append(Wall())
        walls[len(walls) - 1].rect.center = [0 + i * 25, 500]

    for p in points:
        PointsSprs.add(p)
    for w in walls:
        WallsSprs.add(w)
    for en in enemies:
        EnemySprs.add(en)


load()
#
running = True
state = 0
while running:
    clock.tick(FPS)
    ###################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and state == 0:
                player.direction = [-1, 0]
            if event.key == pygame.K_RIGHT and state == 0:
                player.direction = [1, 0]
            if event.key == pygame.K_DOWN and state == 0:
                player.direction = [0, 1]
            if event.key == pygame.K_UP and state == 0:
                player.direction = [0, -1]
            if event.key == pygame.K_r or event.key == pygame.K_f:
                state = 0
                load()
    ###################
    if state == 0:
        # all_sprites.update()
        player.update()
        for e in enemies:
            e.update()

        text = font.render(str(player.points_count), False, (255, 0, 0))
        ###################
        screen.fill(BLACK)

        PointsSprs.draw(screen)
        PlayerSprs.draw(screen)
        WallsSprs.draw(screen)
        EnemySprs.draw(screen)
        screen.blit(down_bar, [0, 500])
        if player.points_count < 10:
            screen.blit(text, [245, 545])
        elif player.points_count < 100:
            screen.blit(text, [240, 545])
        else:
            screen.blit(text, [230, 545])
        if player.points_count >= 100:
            state = 2
    elif state == 1:
        # screen.fill(BLACK)
        screen.blit(fail, [50, 5])
    elif state == 2:
        screen.blit(win, [50, 5])

    pygame.display.update()

pygame.quit()

