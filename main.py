import os
from classes import *

#
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Student-Man")
clock = pygame.time.Clock()
#
game_folder = os.path.dirname(__file__)
data_folder = os.path.join(game_folder, 'data')
player_img = pygame.image.load(os.path.join(data_folder, 'run-0.png')).convert()
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

dot = [pygame.image.load(os.path.join(data_folder, 'dot1.png')).convert(),
       pygame.image.load(os.path.join(data_folder, 'dot2.png')).convert(),
       pygame.image.load(os.path.join(data_folder, 'dot3.png')).convert()]
for d in dot:
    d.set_colorkey(BLACK)

pygame.display.set_icon(icon)
font = pygame.font.SysFont('Comic Sans MS', 30)
font2 = pygame.font.SysFont('Comic Sans MS', 16)

player = Player((player_img, run1img, run2img), dot[2])
PlayerSprs.add(player)
#
walls = []
enemies = []
points = []


def load():
    loadlevel()

    walls.clear()
    enemies.clear()
    points.clear()
    WallsSprs.empty()
    EnemySprs.empty()
    PointsSprs.empty()

    player.__init__((player_img, run1img, run2img), dot[2])
    # points
    rndm = []
    for r in range(0, len(Level)):
        for c in range(0, len(Level[r])):
            if Level[r][c] != 1:
                rndm.append([r, c])

    random.shuffle(rndm)
    rndm = rndm[:15]
    for ri in rndm:
        Level[ri[0]][ri[1]] = 2
    for pi in range(0, 15):
        points.append(Point(point))
        # points[len(points) - 1].rect.center = [random.randint(2, 18) * 25, random.randint(2, 18) * 25]
        points[len(points) - 1].rect.center = [rndm[len(points) - 1][0] * 25, rndm[len(points) - 1][1] * 25]
        if pi >= 10:
            points[len(points) - 1].value = 10
            points[len(points) - 1].image = two_points

    # enemies
    enemies.append(Enemy(enemy, dot[0]))
    enemies[len(enemies) - 1].rect.center = [150, 50]
    enemies.append(Enemy(enemy, dot[1]))
    enemies[len(enemies) - 1].rect.center = [300, 50]

    # walls
    for r in range(0, len(Level)):
        for c in range(0, len(Level[r])):
            if Level[r][c] == 1:
                walls.append(Wall(wall))
                walls[len(walls) - 1].rect.center = [r * 25, c * 25]

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
alg = 1
way = 1

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
            if event.key == pygame.K_x:
                way += 1
                if way > 2:
                    way = 1
            if event.key == pygame.K_c:
                alg += 1
                if alg > 4:
                    alg = 1
            if event.key == pygame.K_z:
                alg -= 1
                if alg < 1:
                    alg = 4
    ###################
    if state == 0:
        # all_sprites.update()
        state = player.update()

        #

        text = font.render(str(player.points_count), False, (255, 0, 0))

        text2 = font.render("DFS", False, (0, 0, 0))
        if alg == 2:
            text2 = font.render("BFS", False, (0, 0, 0))
        elif alg == 3:
            text2 = font.render("UCS", False, (0, 0, 0))
        elif alg == 4:
            text2 = font.render("A*", False, (0, 0, 0))
        text3 = font.render("PATH", False, (0, 0, 0))
        if way == 2:
            text3 = font.render("VSTD", False, (0, 0, 0))
        ###################
        screen.fill(BLACK)

        for e in enemies:
            e.update(Level, player.dot, alg, way, screen, font)

            if e.route:
                for r_dot in e.route:
                    screen.blit(e.dot_img, [r_dot[0] * 25 - 12.5, r_dot[1] * 25 - 12.5])

        if player.route:
            for r_dot in player.route:
                screen.blit(player.dot_img, [r_dot[0] * 25 - 12.5, r_dot[1] * 25 - 12.5])

        PointsSprs.draw(screen)
        PlayerSprs.draw(screen)
        WallsSprs.draw(screen)
        EnemySprs.draw(screen)
        screen.blit(down_bar, [0, 500])
        for e in enemies:
            text4 = font2.render(str(e.timer), False, (255, 255, 255))
            screen.blit(text4, [e.rect[0], e.rect[1]+25])
        #

        screen.blit(text, [250-font.size(str(player.points_count))[0]/2, 545])
        # if player.points_count < 10:
        #     screen.blit(text, [245, 545])
        # elif player.points_count < 100:
        #     screen.blit(text, [240, 545])
        # else:
        #     screen.blit(text, [230, 545])
        #
        screen.blit(text2, [370, 500])
        screen.blit(text3, [370, 550])
    elif state == 1:
        # screen.fill(BLACK)
        screen.blit(fail, [50, 5])
    elif state == 2:
        screen.blit(win, [50, 5])

    # running = False
    pygame.display.update()
    # state = 3

pygame.quit()
