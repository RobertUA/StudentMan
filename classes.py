from levels import *
from algs import *


class Point(pygame.sprite.Sprite):
    def __init__(self, point):
        pygame.sprite.Sprite.__init__(self)
        self.value = 5
        self.image = point
        self.rect = self.image.get_rect()
        self.rect.center = [-100, 0]


class Wall(pygame.sprite.Sprite):
    def __init__(self, wall):
        pygame.sprite.Sprite.__init__(self)
        self.image = wall
        self.rect = self.image.get_rect()
        self.rect.center = [-100, 0]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy, dot_img):
        pygame.sprite.Sprite.__init__(self)
        self.direction = [-1, 0]
        self.steps = 0
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.center = [-100, 0]
        self.dot = []
        self.dot_img = dot_img
        self.route = None
        self.timer = ""

    def update(self, level, player_dot, alg, way, screen, font):
        temp_rect = self.rect
        if self.steps > 0:
            self.steps -= 1
            temp_rect.x += self.direction[0]
            temp_rect.y += self.direction[1]
        else:
            temp_dot = [self.rect.center[0] / 25, self.rect.center[1] / 25]
            if 0 <= temp_dot[0] <= 20 and 0 <= temp_dot[1] <= 20:
                self.dot = temp_dot
            # print(self.dot)

            if self.rect.center[0] % 25 != 0 or self.rect.center[1] % 25 != 0:
                print(self.rect.center)
            # rnd = random.randint(0, 35)
            # if rnd == 0:
            #     self.direction = [1, 0]
            # elif rnd == 1:
            #     self.direction = [-1, 0]
            # elif rnd == 2:
            #     self.direction = [0, 1]
            # elif rnd == 3:
            #     self.direction = [0, -1]
            # print(self.rect.center)
            self.steps = 25
            # collision
            nextdot = [int(self.dot[0] + self.direction[0]), int(self.dot[1] + self.direction[1])]
            if 0 <= nextdot[0] <= 20 and 0 <= nextdot[1] <= 20:
                if Level[nextdot[0]][nextdot[1]] == 1:
                    self.direction = [0, 0]

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
            #
            route = []
            start_timer()
            if alg == 1:
                route = dfs(Level, player_dot, self.dot)
            elif alg == 2:
                route = bfs(Level, player_dot, self.dot)
            elif alg == 3:
                route = ucs(Level, player_dot, self.dot)
            elif alg == 4:
                route = astar(Level, player_dot, self.dot)
            self.timer = str(end_timer())

            temp_dir = [route[0][-2][0]-self.dot[0], route[0][-2][1]-self.dot[1]]
            if -1 <= temp_dir[0] <= 1 and -1 <= temp_dir[1] <= 1:
                self.direction = temp_dir
            if route is not None:
                if way == 1:
                    self.route = route[0]
                elif way == 2:
                    self.route = route[1]


class Player(pygame.sprite.Sprite):
    def __init__(self, sprites, dot_img):
        pygame.sprite.Sprite.__init__(self)
        self.dot = [0, 0]
        self.dot_img = dot_img
        self.points_count = 0
        self.image = sprites[0]
        self.iter = 0
        self.rect = self.image.get_rect()
        self.rect.center = [50, 450]
        self.sprites = (sprites[0], sprites[1], sprites[2], sprites[1])
        self.nextanim = 0
        self.direction = [1, 0]
        self.oldDirection = [1, 0]
        self.steps = 0
        self.route = []

    def update(self):
        # death
        enemy_hit = pygame.sprite.spritecollide(self, EnemySprs, False)
        if enemy_hit:
            return 1
        # points
        points_hit = pygame.sprite.spritecollide(self, PointsSprs, True)
        if points_hit:
            Level[self.dot[0] + self.direction[0]][self.dot[1] + self.direction[1]] = 0
            for el in points_hit:
                self.points_count += el.value
            # print(self.points_count)
            if self.points_count >= 100:
                return 2
        # temp
        temp_rect = self.rect

        if self.steps > 0:
            self.steps -= 1
            temp_rect.x += self.oldDirection[0]
            temp_rect.y += self.oldDirection[1]
        else:
            temp_dot = [self.rect.center[0] / 25, self.rect.center[1] / 25]
            if 0 <= temp_dot[0] <= 20 and 0 <= temp_dot[1] <= 20:
                self.dot = [int(temp_dot[0]), int(temp_dot[1])]
            # print(self.rect.center)
            self.steps = 25
            # collision
            coin = bfs_find_closest_point(Level, self.dot)
            target = astar(Level, coin, self.dot)
            self.route = target[0]
            if self.dot != target[0][0]:
                temp_dir = target[0][-2][0] - self.dot[0], target[0][-2][1] - self.dot[1]
                # print(temp_dir)
                if -1 <= temp_dir[0] <= 1 and -1 <= temp_dir[1] <= 1:
                    self.direction = temp_dir
            self.oldDirection = self.direction
            # print(self.direction)
            nextdot = [int(self.dot[0] + self.oldDirection[0]), int(self.dot[1] + self.oldDirection[1])]
            if 0 <= nextdot[0] <= 20 and 0 <= nextdot[1] <= 20:
                if Level[nextdot[0]][nextdot[1]] == 1:
                    self.oldDirection = [0, 0]
        # anim
        self.iter += 1
        if self.iter % 10 == 0 and self.oldDirection != [0, 0]:
            self.iter = 0
            if self.nextanim > 2:
                self.nextanim = 0
            else:
                self.nextanim += 1
        self.image = self.sprites[self.nextanim]
        if self.direction[0] < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        # borders
        if temp_rect.left > WIDTH and self.oldDirection[0] == 1:
            temp_rect.x = -24
        elif temp_rect.right < 0 and self.oldDirection[0] == -1:
            temp_rect.x = WIDTH - 1
        elif temp_rect.top < 0 and self.oldDirection[1] == -1:
            temp_rect.y = HEIGHT - 1
        elif temp_rect.bottom > HEIGHT and self.oldDirection[1] == 1:
            temp_rect.y = -24
        # move
        self.rect = temp_rect
        return 0
