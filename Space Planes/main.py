import pygame
import os
import random
import sys


pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 750, 550
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Planes")
ICON = pygame.image.load(os.path.join("Assets", "Game_Icon.png"))
pygame.display.set_icon(ICON)

PLAYER_WIDTH, PLAYER_HEIGHT = 65, 55
ENEMY_WIDTH, ENEMY_HEIGHT = 65, 55
LASER_WIDTH, LASER_HEIGHT = 25, 55
FPS = 60

GENERAL_FONT = pygame.font.SysFont('comicsans', 35)
LOST_FONT = pygame.font.SysFont('comicsans', 70)

# Images
BACKGROUND = pygame.image.load(os.path.join("Assets", "Background.png"))
PLAYER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Player.png")), (PLAYER_WIDTH, PLAYER_HEIGHT))

BLUE_ENEMY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Blue_Enemy.png")),
                                    (ENEMY_WIDTH, ENEMY_HEIGHT))
RED_ENEMY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Red_Enemy.png")),
                                   (ENEMY_WIDTH, ENEMY_HEIGHT))
YELLOW_ENEMY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Yellow_Enemy.png")),
                                      (ENEMY_WIDTH, ENEMY_HEIGHT))
PURPLE_ENEMY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Purple_Enemy.png")),
                                      (ENEMY_WIDTH, ENEMY_HEIGHT))

BLUE_LASER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Blue_Laser.png")),
                                    (LASER_WIDTH, LASER_HEIGHT))
RED_LASER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Red_Laser.png")),
                                   (LASER_WIDTH, LASER_HEIGHT))
YELLOW_LASER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Yellow_Laser.png")),
                                      (LASER_WIDTH, LASER_HEIGHT))
PURPLE_LASER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Purple_Laser.png")),
                                      (LASER_WIDTH, LASER_HEIGHT))

PLAYER_LASER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Player_Laser.png")),
                                      (LASER_WIDTH, LASER_HEIGHT))

LIVES_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Lives.png")), (50, 50))

ships = []
player_bullets = []
MAX_BULLETS = 1

ENEMY_SPEED = 3.5
BULLET_VELOCITY = 8
PLAYER_VELOCITY = 8

# Colors
DARK_BLUE = (50, 70, 168)
WHITE = (255, 255, 255)

SPAWN_SHIP_EVENT = pygame.USEREVENT + 1
SHIP_HIT = pygame.USEREVENT + 2
SHIP_DESTROYED = pygame.USEREVENT + 3
PLAYER_HIT = pygame.USEREVENT + 4

# Sounds

BULLET_HIT = pygame.mixer.Sound(os.path.join("Assets", "Bullet_Hit.wav"))
BULLET_FIRE = pygame.mixer.Sound(os.path.join("Assets", "Bullet_Fire.wav"))
BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join("Assets", "Background_Music.mp3"))
HEALTH_UP = pygame.mixer.Sound(os.path.join("Assets", "Health_Up.wav"))
GAME_OVER = pygame.mixer.Sound(os.path.join("Assets", "Game_Over.wav"))


def spawn_ship():
    random_ship = random.randint(1, 4)
    ship_x = random.randint(50,
                            WIDTH - ENEMY_WIDTH - 40)  # Random x position for the ship with a difference of the ship's width -10
    ship_y = -20
    ship_position = (pygame.Rect(ship_x, ship_y, ENEMY_WIDTH, ENEMY_HEIGHT),
                     random_ship)  # the random int will be used to determine a random ship color to spawn
    ships.append(ship_position)


def player_movement_handler(keys_pressed, player):
    # WASD movement and Arrow keys movement
    if keys_pressed[pygame.K_a] and player.x + 15 > 0 or keys_pressed[
        pygame.K_LEFT] and player.x + 15 > 0:  # Moves the player and also sets the window borders
        player.x -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_d] and player.x + PLAYER_WIDTH - 15 < WIDTH or keys_pressed[
        pygame.K_RIGHT] and player.x + PLAYER_WIDTH - 15 < WIDTH:
        player.x += PLAYER_VELOCITY
    if keys_pressed[pygame.K_w] and player.y > 0 or keys_pressed[pygame.K_UP] and player.y > 0:
        player.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_s] and player.y + PLAYER_HEIGHT < HEIGHT or keys_pressed[
        pygame.K_DOWN] and player.y + PLAYER_HEIGHT < HEIGHT:
        player.y += PLAYER_VELOCITY


def player_bullet_handler(bullets, ships_list):
    for bullet in bullets:
        bullet.y -= BULLET_VELOCITY
        for ship in ships:
            bullet_collider = pygame.Rect.colliderect(bullet, ship[0])

            if bullet_collider and len(bullets) > 0:
                BULLET_HIT.set_volume(0.3)
                BULLET_HIT.play()

                ships_list.remove(ship)
                bullets.remove(bullet)

                pygame.event.post(pygame.event.Event(SHIP_DESTROYED))
            if bullet.y < 0 and len(bullets) > 0:
                bullets.remove(bullet)


def ship_collider(ships_list, player_rectangle):  # Handles if ship goes under the screen.
    for ship in ships_list:
        ship_player_collider = pygame.Rect.colliderect(player_rectangle, ship[0])

        if ship_player_collider:
            ships_list.remove(ship)
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
            BULLET_HIT.play()

        if ship[0].y + ENEMY_HEIGHT > HEIGHT:  # If ship goes outside the frame -1 hitpoints
            pygame.event.post(pygame.event.Event(SHIP_HIT))
            ships_list.remove(ship)

def draw_display(player_rect, lives, points, ship, player_bullet):
    WIN.blit(BACKGROUND, (0, 0))

    WIN.blit(PLAYER, (player_rect.x, player_rect.y))

    WIN.blit(LIVES_IMAGE, (5, 5))
    WIN.blit(lives, (50, 10))
    WIN.blit(points, (WIDTH - points.get_width() - 10, 10))

    for bullet in player_bullet:
        WIN.blit(PLAYER_LASER, (bullet.x, bullet.y))

    for enemy in ship:
        if enemy[1] == 1:  # if the random int inside the tuple is 1 then spawn a blue ship
            WIN.blit(BLUE_ENEMY, (enemy[0].x, enemy[0].y))
        if enemy[1] == 2:
            WIN.blit(RED_ENEMY, (enemy[0].x, enemy[0].y))
        if enemy[1] == 3:
            WIN.blit(YELLOW_ENEMY, (enemy[0].x, enemy[0].y))
        if enemy[1] == 4:
            WIN.blit(PURPLE_ENEMY, (enemy[0].x, enemy[0].y))

    pygame.display.update()


def main():
    BACKGROUND_MUSIC.play(-1)
    BACKGROUND_MUSIC.set_volume(0.35)
    ships.clear()

    SPAWNING_INTERVAL = 820
    pygame.time.set_timer(SPAWN_SHIP_EVENT, SPAWNING_INTERVAL)

    nr_lives = 5
    points = 0



    run = True
    player_rect = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - 100, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == SPAWN_SHIP_EVENT:
                spawn_ship()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_bullets) < MAX_BULLETS:
                    bullet_pos = pygame.Rect(player_rect.x + 20, player_rect.y - 27, LASER_WIDTH, LASER_HEIGHT)
                    player_bullets.append(bullet_pos)

                    BULLET_FIRE.set_volume(1)
                    BULLET_FIRE.play()

            if event.type == SHIP_HIT:
                nr_lives -= 1
            if event.type == SHIP_DESTROYED:
                points += 1
            if event.type == PLAYER_HIT:
                nr_lives -= 1

        for ship in ships:  # Moves the ship
            ship[0].y += ENEMY_SPEED

        if points % 20 == 0 and points != 0:
            nr_lives += 1
            points += 1
            HEALTH_UP.play()

        if nr_lives <= 0:
            GAME_OVER.play()
            break

        points_text = GENERAL_FONT.render("Points : " + str(points), True, WHITE)
        lives_text = GENERAL_FONT.render(str(nr_lives), True, WHITE)

        keys_pressed = pygame.key.get_pressed()
        player_movement_handler(keys_pressed, player_rect)
        player_bullet_handler(player_bullets, ships)
        ship_collider(ships, player_rect)
        draw_display(player_rect, lives_text, points_text, ships, player_bullets)

    BACKGROUND_MUSIC.stop()
    main()


try:
    if __name__ == "__main__":  # Runs the main loop and assures it can only be run directly
        main()
except:
    print("Oops!", sys.exc_info()[0], "occurred.")
