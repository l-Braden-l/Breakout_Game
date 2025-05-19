import pygame
import random


# -- Window Dimensions and Title -- # 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = 'Simple Breakout Game'
FPS = 30

# -- Colors -- # 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# -- Font -- # 
FONT = 'Ariel'
FONT_SIZE_SCORE = 36
FONT_SIZE_START = 36
FONT_SIZE_INSTRUCTIONS = 24
FONT_SIZE_GAMEOVER_TITLE = 48
FONT_SIZE_GAMEOVER_SCORE = 36
FONT_SIZE_GAMEOVER_RESTART = 26

# -- Player Constants -- # 
PLAYER_WIDTH = 200 
PLAYER_HEIGHT = 20 
PLAYER_START_X = SCREEN_WIDTH // 2 
PLAYER_START_Y = SCREEN_HEIGHT - 40
PLAYER_MOVEMENT_SPEED = 30

# -- Ball Constants -- # 
BALL_RADIUS = 10 
BALL_DIAMETER = BALL_RADIUS * 2 
BALL_START_X = SCREEN_WIDTH // 2
BALL_START_Y = SCREEN_HEIGHT // 2 
BALL_INITIAL_X_SPEED = 10 
BALL_INITIAL_Y_SPEED = 12

# -- Brick Constants -- # 
BRICK_WIDTH = 100 
BRICK_HEIGHT = 30
BRICK_HORIZONTIAL_PADDING = 50 
BRICK_VERTICAL_PADDING = 20
BRICK_ROWS = 6 
BRICK_COLUMNS = 8 


class Player(pygame.sprite.Sprite): 
    """Represents the player's paddle."""

    def __init__(self, color):
        super().__init__()
        self.color = color 
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # - Position (X, Y) - # 
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.rect.center = (self.x, self.y)

    def update(self):
        """Moves the player based on keyboard input."""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.x <= SCREEN_WIDTH - PLAYER_WIDTH // 2 and self.y > SCREEN_HEIGHT - 100: 
            self.x += PLAYER_MOVEMENT_SPEED
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.x >= PLAYER_WIDTH // 2 and self.y > SCREEN_HEIGHT - 100: 
            self.x -= PLAYER_MOVEMENT_SPEED

        self.rect.center = (self.x, self.y)


class Ball(pygame.sprite.Sprite): 
    """Represents the Ball"""
    def __init__(self):
        super().__init__()
        ball_image = pygame.Surface((BALL_DIAMETER, BALL_DIAMETER))
        pygame.draw.circle(ball_image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        

        self.image = ball_image 
        self.rect = self.image.get_rect()

        # - Position (X, Y) and Velocity - #
        self.x = BALL_START_X
        self.y = BALL_START_Y
        self.x_vel = BALL_INITIAL_X_SPEED
        self.y_vel = BALL_INITIAL_Y_SPEED
        self.rect.center = (self.x, self.y)

    def update(self): 
        """Moves the ball and handles boucning off walls."""
        self.x += self.x_vel
        self.y += self.y_vel

        if self.x <= BALL_RADIUS or self.x > SCREEN_WIDTH - BALL_RADIUS: 
            self.x_vel *= -1 # - Reverse Horizontal Direction - # 

        if self.y <= BALL_RADIUS: 
            self.y_vel *= -1 # - Reverse Vertical Direction - # 

        self.rect.center = (self.x, self.y)


class Brick(pygame.sprite.Sprite):
    """Represents a brick in the game."""

    def __init__(self, x, y, color): 
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Game: 
    """Managest the overall game logic and states."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True # - Flag to keep the game running - # 
        self.font_name = pygame.font.match_font(FONT)

    def new(self): 
        """Sets up a new game."""

        self.all_sprites = pygame.sprite.Group() # - Group to hold all sprites - # 
        self.players = pygame.sprite.Group() # - Group to hold the player - # 
        self.bricks = pygame.sprite.Group() # - Group to hold the bricks - # 
        self.score = 0 

        self.ball = Ball()
        self.player = Player(WHITE)
        self.all_sprites.add(self.ball)
        self.all_sprites.add(self.player)
        self.players.add(self.player)

        # - Create the Bricks - # 
        for col in range(BRICK_COLUMNS): 
            for row in range(BRICK_ROWS):
                brick_x = BRICK_HORIZONTIAL_PADDING + col * (BRICK_WIDTH + BRICK_HORIZONTIAL_PADDING)
                brick_y = BRICK_VERTICAL_PADDING + row * (BRICK_HEIGHT + BRICK_VERTICAL_PADDING)
                brick = Brick(brick_x, brick_y, BLUE)
                self.all_sprites.add(brick)
                self.bricks.add(brick)

        # - Run the Game - # 
        self.main()

    def main(self): 
        """The main game loop."""

        self.playing = True # - Flag to control the current game session - # 
        while self.playing: 
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self): 
        """Handles game events (e.g., user input, closing of window, etc.)."""

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                self.playing = False 
                self.running = False 

    def update(self): 
        """Updates the game state (e.g., sprite positions, collisions)."""

        self.all_sprites.update()
        
        # - Paddle Check: Handle ball collision with the player's paddle - # 
        hit_paddle = pygame.sprite.spritecollide(self.ball, self.players, False)
        if hit_paddle and self.ball.y_vel > 0: 
            self.ball.y = self.player.rect.top - BALL_RADIUS # - Prevents ball from going into paddle - # 
            self.ball.y_vel *= -1 

        # Brick Check: Handle ball collsions with the player's paddle - # 
        hit_brick = pygame.sprite.spritecollide(self.ball, self.bricks, True)
        if hit_brick: 
            self.ball.y_vel *= -1 
            self.score += len(hit_brick) # - Increase score by the number of bricks hit

            # - Game over condititions - # 
            if self.ball.rect.top > SCREEN_HEIGHT: # - Ball went off the bottom of the screen - #
                self.playing = False
            if not self.bricks: # - No more bricks left
                self.playing = False 
                 
    def draw(self): 
        """Draws the curent game frame."""

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen) # Draw all sprites
        self.draw_text(f'Score: {self.score}', FONT_SIZE_SCORE, RED, SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT - 50) # - Display Score - #

        pygame.display.flip() # - Updates what needs to be drawn on the screen - # 

    def show_start_screen(self):
        """Displays the start screen."""

        self.screen.fill(BLACK)
        self.draw_text('Breakout Game!', FONT_SIZE_START, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        self.draw_text('Press any key to begin...', FONT_SIZE_INSTRUCTIONS, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.flip()
        self.wait_for_key() # - Wait for a key press - # 

    def show_game_over_screen(self): 
        """Displays the game over screen."""

        if not self.running: 
            return 
        self.screen.fill(BLACK)
        self.draw_text ("GAME OVER", FONT_SIZE_GAMEOVER_TITLE, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text (f"Score: {self.score}", FONT_SIZE_GAMEOVER_SCORE, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text = ("Press any key to begin...", FONT_SIZE_GAMEOVER_RESTART, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key() # - Wait for a key press - # 

    def wait_for_key(self):
        """Waits for a key press."""

        waiting = True
        while waiting: 
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False 
                if event.type == pygame.KEYUP: 
                    waiting = False 
    
    def draw_text(self, text, size, color, x, y): 
        """Draws text on the screen."""

        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


# -- Initialize and Run The Game -- #
game = Game()
game.show_start_screen()

while game.running:
    game.new()
    game.show_game_over_screen()

pygame.quit()



    
    
        









