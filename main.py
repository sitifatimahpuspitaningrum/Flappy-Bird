import pygame
import sys
from bird import Bird
from pipe import Pipe
import random

# Inisialisasi
pygame.init()
WIDTH, HEIGHT = 288, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

# Constants
GROUND_Y = 430
TITLE_POS = (44, 200)
INITIAL_GAP = 150
MIN_GAP = 90
NIGHT_MODE_TIME = 10
SPAWN_EVENT = pygame.USEREVENT + 1

# Assets
ASSETS = {
    "day": {
        "bg": pygame.transform.scale(pygame.image.load("assets/Background1.png"), (WIDTH, HEIGHT)),
        "bird": pygame.image.load("assets/redbird-midflap.png"),
        "pipe_top": pygame.image.load("assets/pipe-green-bottom.png"),
        "pipe_bottom": pygame.image.load("assets/pipe-green.png")
    },
    "night": {
        "bg": pygame.transform.scale(pygame.image.load("assets/Background2.png"), (WIDTH, HEIGHT)),
        "bird": pygame.image.load("assets/yellowbird-midflap.png"),
        "pipe_top": pygame.image.load("assets/pipe-red-bottom.png"),
        "pipe_bottom": pygame.image.load("assets/pipe-red.png")
    }
}
ground = pygame.image.load("assets/base.png")
title_img = pygame.transform.scale(pygame.image.load("assets/Font1.png"), (200, 50))
game_over_img = pygame.transform.scale(pygame.image.load("assets/Font2.png"), (200, 50))

def show_screen(image, pos, key):
    while True:
        screen.blit(ASSETS["day"]["bg"], (0, 0))
        screen.blit(image, pos)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == key:
                return

def main_game():
    score = 0
    mode = "day"
    bird = Bird(50, 250, ASSETS[mode]["bird"])
    pipes = []
    start_time = pygame.time.get_ticks()
    game_over = False
    pygame.time.set_timer(SPAWN_EVENT, 1500)

    while not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        mode = "night" if elapsed_time > NIGHT_MODE_TIME else "day"

        if bird.image != ASSETS[mode]["bird"]:
            bird.image = ASSETS[mode]["bird"]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()
            if event.type == SPAWN_EVENT:
                height = random.randint(100, 300) if mode == "night" else 200
                difficulty_time = min(elapsed_time // 10, 6)
                difficulty_score = min(score // 5, 6)  
                gap = INITIAL_GAP - (difficulty_time * 10 + difficulty_score * 5)
                gap = max(gap, MIN_GAP)
                pipes.append(Pipe(288, height, ASSETS[mode]["pipe_top"], ASSETS[mode]["pipe_bottom"], gap, night_mode=(mode == "night")))

        bird.update()
        for pipe in pipes:
            pipe.move()
            if pipe.x + pipe.pipe_top.get_width() < bird.x and not pipe.scored:
                score += 1
                pipe.scored = True
            if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                game_over = True
        if bird.rect.bottom >= GROUND_Y: 
            game_over = True

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x + pipe.pipe_top.get_width() > -50]

        # Draw
        screen.blit(ASSETS[mode]["bg"], (0, 0))
        for pipe in pipes:
            pipe.draw(screen)
        bird.draw(screen)
        screen.blit(ground, (0, GROUND_Y))
        time_text = font.render(f"Time: {int(elapsed_time)}s", True, (0, 0, 0))
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))  
        screen.blit(time_text, (10, 10))
        screen.blit(score_text, (10, 40))

        pygame.display.update()
        clock.tick(60)

def main():
    while True:
        show_screen(title_img, TITLE_POS, pygame.K_SPACE)
        main_game()
        show_screen(game_over_img, TITLE_POS, pygame.K_r)

if __name__ == "__main__":
    main()