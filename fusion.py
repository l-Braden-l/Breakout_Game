import pygame
import sys

# -- Constants -- #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
TITLE = 'Simple Breakout Game'
FPS = 30
FONT = 'Arial'

# Player Constants
PLAYER_WIDTH = 200
PLAYER_HEIGHT = 20
PLAYER_START_X = WINDOW_WIDTH // 2
PLAYER_START_Y = WINDOW_HEIGHT - 40
PLAYER_MOVEMENT_SPEED = 30

# Ball Constants
BALL_RADIUS = 10
BALL_DIAMETER = BALL_RADIUS * 2
BALL_START_X = WINDOW_WIDTH // 2
BALL_START_Y = WINDOW_HEIGHT // 2
BALL_INITIAL_X_SPEED = 10
BALL_INITIAL_Y_SPEED = 12

# Brick Constants
BRICK_WIDTH = 100
BRICK_HEIGHT = 30
BRICK_HORIZONTIAL_PADDING = 50
BRICK_VERTICAL_PADDING = 20
BRICK_ROWS = 5
BRICK_COLUMNS = 8


# -- Game Classes -- #
class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.rect.center = (self.x, self.y)


    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x <= WINDOW_WIDTH - PLAYER_WIDTH // 2:
            self.x += PLAYER_MOVEMENT_SPEED
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x >= PLAYER_WIDTH // 2:
            self.x -= PLAYER_MOVEMENT_SPEED
        self.rect.center = (self.x, self.y)

    def set_width(self, new_width):
        old_center = self.rect.center
        self.image = pygame.Surface((new_width, PLAYER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = old_center


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ball_image = pygame.Surface((BALL_DIAMETER, BALL_DIAMETER), pygame.SRCALPHA)
        pygame.draw.circle(ball_image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.x = BALL_START_X
        self.y = BALL_START_Y
        self.x_vel = BALL_INITIAL_X_SPEED
        self.y_vel = BALL_INITIAL_Y_SPEED
        self.rect.center = (self.x, self.y)

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        if self.x <= BALL_RADIUS or self.x >= WINDOW_WIDTH - BALL_RADIUS:
            self.x_vel *= -1
        if self.y <= BALL_RADIUS:
            self.y_vel *= -1
        self.rect.center = (self.x, self.y)

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT)

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.score = 0
        self.ball = Ball()
        self.player = Player(WHITE)
        self.all_sprites.add(self.ball, self.player)
        self.players.add(self.player)

        for col in range(BRICK_COLUMNS):
            for row in range(BRICK_ROWS):
                brick_x = BRICK_HORIZONTIAL_PADDING + col * (BRICK_WIDTH + BRICK_HORIZONTIAL_PADDING)
                brick_y = BRICK_VERTICAL_PADDING + row * (BRICK_HEIGHT + BRICK_VERTICAL_PADDING)
                brick = Brick(brick_x, brick_y, BLUE)
                self.all_sprites.add(brick)
                self.bricks.add(brick)

        self.main()

    def main(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        if pygame.sprite.spritecollide(self.ball, self.players, False) and self.ball.y_vel > 0:
            self.ball.y = self.player.rect.top - BALL_RADIUS
            self.ball.y_vel *= -1

        hit_brick = pygame.sprite.spritecollide(self.ball, self.bricks, True)
        if hit_brick:
            self.ball.y_vel *= -1
            self.score += len(hit_brick)

            # Shrink paddle based on score
            new_width = max(60, PLAYER_WIDTH - self.score * 5)  # never smaller than 60
            self.player.set_width(new_width)

        if self.ball.rect.top > WINDOW_HEIGHT or not self.bricks:
            self.playing = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(f'Score: {self.score}', 36, RED, WINDOW_WIDTH * 3 / 4, WINDOW_HEIGHT - 50)
        pygame.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_game_over_screen(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
        self.draw_text(f"Score: {self.score}", 36, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.draw_text("Press any key to return to menu", 26, WHITE, WINDOW_WIDTH / 2, WINDOW_HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

# -- Main Menu -- #
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    # --Backgroud image for menu -- #
    MBACKGROUND = pygame.image.load("C:\\brickbreaker\\bright-green-brick-wall-background-vector-27145091.jpg").convert()
    BACKGROUND_POSITION = [0,0]
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 40)
    header = font.render("Main Menu", True, BLUE)

    button_length = 200
    button_height = 50
    button_x = (WINDOW_WIDTH - button_length) // 2
    button1 = pygame.Rect(button_x, 200, button_length, button_height)
    button2 = pygame.Rect(button_x, 270, button_length, button_height)
    button3 = pygame.Rect(button_x, 340, button_length, button_height)

    button1_text = font.render('PLAY', True, BLACK)
    button2_text = font.render('OPTIONS', True, BLACK)
    button3_text = font.render('EXIT', True, BLACK)

    while True:
        screen.blit(MBACKGROUND, BACKGROUND_POSITION)
        screen.blit(header, (WINDOW_WIDTH // 2 - header.get_width() // 2, 120))

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button1.collidepoint(mouse_pos):
                        return 'play'
                    elif button2.collidepoint(mouse_pos):
                        print("Options selected")
                    elif button3.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

        # Button colors
        def hover_color(rect):
            return (0, 255, 0) if rect.collidepoint(mouse_pos) else (90, 255, 90)

        pygame.draw.rect(screen, hover_color(button1), button1)
        pygame.draw.rect(screen, hover_color(button2), button2)
        pygame.draw.rect(screen, hover_color(button3), button3)

        screen.blit(button1_text, (button1.x + (button_length - button1_text.get_width()) // 2, button1.y + 5))
        screen.blit(button2_text, (button2.x + (button_length - button2_text.get_width()) // 2, button2.y + 5))
        screen.blit(button3_text, (button3.x + (button_length - button3_text.get_width()) // 2, button3.y + 5))

        pygame.display.flip()
        clock.tick(FPS)

# -- Main Loop -- #
while True:
    menu_action = main_menu()
    if menu_action == 'play':
        game = Game()
        game.new()
        game.show_game_over_screen()



#.fill(