# -- Imports -- #
import pygame
import sys

# -- Constants -- #
   # - Colors - # 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (153, 76, 0)
PURPLE = (204, 0, 204)
ORANGE =  (255, 128, 0)
SKY_BLUE = (0, 255, 255)

   # - Widow - #
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

   # - Title - # 
TITLE = "Button Menu"

   # - Frame Rate - #
FPS = 60


def init_game (): 
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()  # Initialize the mixer
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Use constants from config
    pygame.display.set_caption(TITLE)
    return screen

# -- Button Click Function -- # 
def button_Click_func(): 
   button_click = pygame.mixer.Sound('c:\\sounds\\button-pressed-38129.mp3')  
   pygame.mixer.Sound.play(button_click) 


# -- Button Hover Function -- # 
def button_hover_func(): 
   button_hover = pygame.mixer.Sound("C:\\sounds\\button-305770.mp3")  
   pygame.mixer.Sound.play(button_hover) 


def main():
   screen = init_game()
   clock = pygame.time.Clock()  # Initialize the clock here

   # -- Font -- #
   font_style = pygame.font.SysFont("Arial", 40)
   header = font_style.render("Main Menu", True, BLUE)

   # -- Button Variables -- #
   button_length = 200
   button_height = 50
   button_x = 280
   button1 = pygame.Rect(button_x, 200, button_length, button_height)
   button2 = pygame.Rect(button_x, 270, button_length, button_height)
   button3 = pygame.Rect(button_x, 340, button_length, button_height)

   # -- Button Text -- #
   button1_text = font_style.render('PLAY', True, BLACK)
   button2_text = font_style.render('OPTIONS', True, BLACK)
   button3_text = font_style.render('EXIT', True, BLACK)

   # -- Update Menu -- #
   headx = 300 

    # -- Load and Set Up Graphic -- #
   background_image = pygame.image.load("C:\Project-Text-Menu\Pixel_Art_Background.png").convert()


   running = True
   while running:
      mouse_pos = pygame.mouse.get_pos()

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
               if button1.collidepoint(mouse_pos):
                  print("Now playing the game!")
                  button_Click_func()
                  button1.x = -500
                  button2.x = -500
                  button3.x = -500
                  headx = -300 
                  screen.blit(background_image, [0,0])
            
                    # Play the sound when clicked
               elif button2.collidepoint(mouse_pos):
                  print("Game options!")
                  button_Click_func()
               elif button3.collidepoint(mouse_pos):
                  button_Click_func()
                  pygame.quit()
                  sys.exit()
            else: 
               screen.fill(WHITE)
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               return False

      # Button hover logic
      if button1.collidepoint(mouse_pos):
         button_color1 = (0, 255, 0)
      else:
         button_color1 = (90, 255, 90)
         
      if button2.collidepoint(mouse_pos):
         button_color2 = (0, 255, 0)
      else:
         button_color2 = (90, 255, 90)

      if button3.collidepoint(mouse_pos): 
         button_color3 = (0, 255, 0)
      else:
         button_color3 = (90, 255, 90)

      screen.blit(header, (headx, 150))

      # Draw Rectangles
      pygame.draw.rect(screen, button_color1, button1)
      pygame.draw.rect(screen, button_color2, button2)
      pygame.draw.rect(screen, button_color3, button3)

      # Fit Text on Button
      screen.blit(button1_text, (button1.x + (button_length - button1_text.get_width()) // 2, button1.y + (button_height - button1_text.get_height()) // 2))
      screen.blit(button2_text, (button2.x + (button_length - button2_text.get_width()) // 2, button2.y + (button_height - button2_text.get_height()) // 2))
      screen.blit(button3_text, (button3.x + (button_length - button3_text.get_width()) // 2, button3.y + (button_height - button3_text.get_height()) // 2))

      pygame.display.flip()

      # Limit the frame rate to the specified frames per second (FPS)
      clock.tick(FPS)

   pygame.quit()
   sys.exit()

if __name__ == "__main__":
   main()