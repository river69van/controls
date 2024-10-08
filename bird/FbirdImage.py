import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH = 1080
HEIGHT = 720 
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
PIPE_WIDTH = 50
PIPE_HEIGHT = 500
PIPE_GAP = 130  # Increase the gap size for the hole
GRAVITY = 1
JUMP_STRENGTH = -10
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('123 birds')
clock = pygame.time.Clock()

# Load images
bird_image = pygame.image.load('dddd.png')
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

pipe_image = pygame.image.load('rrrr.png')
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))

class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.vel = 0

    def jump(self):
        self.vel = JUMP_STRENGTH

    def move(self):
        self.vel += GRAVITY
        self.y += self.vel
        if self.y > HEIGHT - BIRD_HEIGHT:
            self.y = HEIGHT - BIRD_HEIGHT
        elif self.y < 0:
            self.y = 0

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.gap_size = PIPE_GAP  # The size of the gap
        self.gap_start = random.randint(100, HEIGHT - self.gap_size - 100)  # Random position for the gap
        self.width = PIPE_WIDTH

    def move(self):
        self.x -= 5

    def draw(self):
        # Draw the top part of the pipe above the gap
        top_pipe = pygame.Surface((self.width, self.gap_start))
        top_pipe.blit(pipe_image, (0, 0))
        screen.blit(top_pipe, (self.x, 0))
        
        # Draw the bottom part of the pipe below the gap
        bottom_pipe = pygame.Surface((self.width, HEIGHT - (self.gap_start + self.gap_size)))
        bottom_pipe.blit(pipe_image, (0, 0))
        screen.blit(bottom_pipe, (self.x, self.gap_start + self.gap_size))

    def off_screen(self):
        return self.x < -self.width

    def collision(self, bird):
        if bird.x + BIRD_WIDTH > self.x and bird.x < self.x + self.width:
            if bird.y < self.gap_start or bird.y + BIRD_HEIGHT > self.gap_start + self.gap_size:
                return True
        return False

def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if not game_over:
            bird.move()
            if pipes[-1].x < WIDTH - 200:
                pipes.append(Pipe())
            if pipes[0].off_screen():
                pipes.pop(0)
                score += 1

            for pipe in pipes:
                pipe.move()
                if pipe.collision(bird):
                    game_over = True

        screen.fill("#AEFFEE") #color
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Display score
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
