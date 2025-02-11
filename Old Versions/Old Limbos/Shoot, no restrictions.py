import pygame
from math import atan2, degrees, pi, sin, cos, tan


pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

screen_width = 500
screen_height = 500

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Limbo")


class Player:
    def __init__(self, x, y, width, height, name):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.left = False
        self.right = False
        self.down = False
        self.up = False

        self.lookUp = [pygame.image.load(self.name + '90.png')]
        self.lookDown = [pygame.image.load(self.name + '270.png')]
        self.lookLeft = [pygame.image.load(self.name + '180.png')]
        self.lookRight = [pygame.image.load(self.name + '0.png')]
        self.lookIdle = [pygame.image.load(self.name + '90.png')]

    def draw(self):
        if self.left:
            win.blit(self.lookLeft[0], (self.x, self.y))

        elif self.right:
            win.blit(self.lookRight[0], (self.x, self.y))

        elif self.down:
            win.blit(self.lookDown[0], (self.x, self.y))

        elif self.up:
            win.blit(self.lookUp[0], (self.x, self.y))

        else:
            win.blit(self.lookIdle[0], (self.x, self.y))


class Projectile:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 10


    def draw(self):
        pygame.draw.circle(win, self.color, (int(round(self.x, 0)), int(round(self.y, 0))), self.radius)


class Bullet(Projectile):
    def __init__(self, x, y, radius, color, velocity):
        super().__init__(x, y, radius, color)
        self.velocity = velocity


guard = Player(100, 100, 40, 60, 'guard')

clock = pygame.time.Clock()
run = True

b = Bullet(guard.x, guard.y, 6, black, 0)


bullets = []


def redrawGameWindow():
    win.fill(green)
    guard.draw()
    for bullet in bullets:
        bullet.draw()
    pygame.display.update()


while run:
    global n

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(bullets) < 6:
                bullets.append(Bullet(guard.x, guard.y, 6, black, 0))

                for bullet in bullets:

                    speed = 10
                    bullet.mouse_position = pygame.mouse.get_pos()
                    bullet.mouse_player_dx = bullet.mouse_position[0] - guard.x
                    bullet.mouse_player_dy = bullet.mouse_position[1] - guard.y
                    bullet.angle = atan2(bullet.mouse_player_dy, bullet.mouse_player_dx)
                    bullet.new_velocity = (speed * cos(bullet.angle), speed * sin(bullet.angle))

                    n = len(bullets) - 1
                    bullets[n].velocity = bullet.new_velocity


    for bullet in bullets:
        if screen_width > bullet.x > 0:

            n = 0
            while n <= len(bullets) - 1:
                bullets[n].x += bullets[n].velocity[0]
                bullets[n].y += bullets[n].velocity[1]
                n += 1

            if screen_width < bullet.x < 0:
                bullets.pop(bullets.index(bullet))

            if screen_height < bullet.y > 0:
                bullets.pop(bullets.index(bullet))

        else:
            bullets.pop(bullets.index(bullet))



    if keys[pygame.K_LEFT] and guard.x > 0:
        guard.x -= guard.speed
        guard.left = True
        guard.right = False
        guard.down = False
        guard.up = False

    if keys[pygame.K_RIGHT] and guard.x + guard.width < screen_width - guard.width:
        guard.x += guard.speed
        guard.left = False
        guard.right = True
        guard.down = False
        guard.up = False

    if keys[pygame.K_UP] and guard.y > 0:
        guard.y -= guard.speed
        guard.left = False
        guard.right = False
        guard.down = False
        guard.up = True

    if keys[pygame.K_DOWN] and guard.y + guard.width < screen_height - guard.height:
        guard.y += guard.speed
        guard.left = False
        guard.right = False
        guard.down = True
        guard.up = False

    redrawGameWindow()
    clock.tick(60)

pygame.quit()
