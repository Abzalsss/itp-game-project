import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 359))
pygame.display.set_caption("Shoot Ghosts")
icon = pygame.image.load("images/iconforscreen.png")
pygame.display.set_icon(icon)

bg = pygame.image.load("images/bg.png").convert_alpha()
walk_left = [
    pygame.image.load("images/player_left/left1.png").convert_alpha(),
    pygame.image.load("images/player_left/left2.png").convert_alpha(),
    pygame.image.load("images/player_left/left3.png").convert_alpha(),
    pygame.image.load("images/player_left/left4.png").convert_alpha()
]

walk_right = [
    pygame.image.load("images/player_right/right1.png").convert_alpha(),
    pygame.image.load("images/player_right/right2.png").convert_alpha(),
    pygame.image.load("images/player_right/right3.png").convert_alpha(),
    pygame.image.load("images/player_right/right4.png").convert_alpha()
]

lose_page = pygame.image.load("images/lose_page.png")

ghost = pygame.image.load("images/ghost.png").convert_alpha()

ghost_list_in_game = []
ghost_count = 0

player_anim_count = 0
bg_x = 0
player_speed = 5
player_x = 150
player_y = 250

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/gamemusic.mp3')
bg_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

label = pygame.font.SysFont('fonts/Roboto-Regular.ttf', 75)
label_game = pygame.font.SysFont('fonts/Roboto-Regular.ttf', 30)

lose_label = label.render("You lose!", True, (255, 255, 255))
restart_label = label.render("Restart!", True, (255, 0, 0))
restart_label_rect = restart_label.get_rect(topleft=(230, 200))

bullets_left = 10
bullet = pygame.image.load("images/bullet.png").convert_alpha()
bullets = []

gameplay = True

start_page = pygame.image.load("images/start_page.png")
start_label = label.render("Start", True, (0, 0, 0))
start_label_rect = start_label.get_rect(topleft=(240, 130))
show_start_page = True
start_button_color = (255, 255, 255)

quit_button_color = (255, 255, 255)
quit_button_hover_color = (255, 100, 100)
quit_label = label.render("Quit", True, (255, 100, 80))
quit_label_rect = quit_label.get_rect(topleft=(240, 190))

player_health = 100
health = label.render("Health: ", True, (255, 255, 255))

score = 0
bullet_count = bullets_left

running = True
while running:
    if show_start_page:
        screen.blit(start_page, (-220, -80))

        pygame.draw.rect(screen, start_button_color, start_label_rect)
        screen.blit(start_label, start_label_rect)
        pygame.draw.rect(screen, quit_button_color, quit_label_rect)
        screen.blit(quit_label, quit_label_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and start_label_rect.collidepoint(event.pos):
                show_start_page = False
            if event.type == pygame.MOUSEBUTTONDOWN and quit_label_rect.collidepoint(
                    event.pos):
                running = False
                pygame.quit()

    else:
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 618, 0))

        if gameplay:
            player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

            if ghost_list_in_game:
                for (i, el) in enumerate(ghost_list_in_game):
                    screen.blit(ghost, el)
                    el.x -= 10

                    if el.x < -10:
                        ghost_list_in_game.pop(i)

                    for (i, el) in enumerate(ghost_list_in_game):
                        if player_rect.colliderect(el):
                            player_health -= 20
                            ghost_list_in_game.pop(i)
                            if player_health <= 0:
                                gameplay = False
                                player_health = 100
                            break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                screen.blit(walk_left[player_anim_count], (player_x, player_y))
            else:
                screen.blit(walk_right[player_anim_count], (player_x, player_y))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 50:
                player_x -= player_speed
            elif keys[pygame.K_RIGHT] and player_x < 300:
                player_x += player_speed

            if not is_jump:
                if keys[pygame.K_UP]:
                    is_jump = True
            else:
                if jump_count >= -8:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2
                    jump_count -= 1
                else:
                    is_jump = False
                    jump_count = 8

            if player_anim_count == 3:
                player_anim_count = 0
            else:
                player_anim_count += 1

            bg_x -= 2
            if bg_x == -618:
                bg_x = 0

            if bullets:
                for (i, el) in enumerate(bullets):
                    screen.blit(bullet, (el.x, el.y))
                    el.x += 6

                    if el.x > 630:
                        bullets.pop(i)

                    if ghost_list_in_game:
                        for (index, ghost_el) in enumerate(ghost_list_in_game):
                            if el.colliderect(ghost_el):
                                ghost_list_in_game.pop(index)
                                bullets.pop(i)
                                score += 10
                                if score % 70 == 0:
                                    bullets_left += 10


        else:
            screen.blit(lose_page, (0, -120))
            screen.blit(lose_label, (220, 120))
            screen.blit(restart_label, restart_label_rect)

            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = True
                player_x = 150
                ghost_list_in_game.clear()
                bullets.clear()
                bullets_left = 10
                score = 0

        health_label = label_game.render("Health: " + str(player_health), True, (255, 255, 255))
        screen.blit(health_label, (10, 10))

        score_label = label_game.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_label, (10, 40))

        bullets_label = label_game.render("Bullets: " + str(bullets_left), True, (255, 255, 255))
        screen.blit(bullets_label, (10, 70))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == ghost_timer:
                ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))
            if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
                bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
                bullets_left -= 1
        clock.tick(15)
