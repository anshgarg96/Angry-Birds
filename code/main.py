import pygame
import engine_classes
import obj_classes
import ctypes
import data
import sys
import tools


clock = pygame.Clock() # Creating clock object for frame rate control
ctypes.windll.user32.SetProcessDPIAware() # The ctypes fix
screen = pygame.display.set_mode((1920,1080)) # Setting Resolution

# Loading image and button
image = pygame.image.load("images/enter screen.jpg") 
enter_button = obj_classes.Button("enter-button.png", (960, 950))

# Welcome Screen Loop
while True:
    x = False
    clock.tick(data.frame_rate) # Maintains Frame rate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        x = enter_button.update(event) # Checking for button click
    if x:
        break # Button Clicked

    # Blit images on to screen for each frame and then display
    screen.blit(image, (0,0))
    screen.blit(enter_button.image, enter_button.rect)
    pygame.display.flip()

image = pygame.image.load("images/home screen 1.jpg")
game_state = 0 # Variable for controlling whether user is at Main Menu, Cradle of Wings or Molten Mayhem
player1_name = None
player2_name = None

# Main Program Loop
while True:
    if game_state == 0:
        # Loading BGM
        pygame.mixer.music.load('sounds/angry-birds.ogg')
        pygame.mixer.music.play()

        # Creating Buttons for selecting Game Mode
        BG1_button = obj_classes.Button("cradle_of_wings (1).png", (300,180), scale = 1.1)
        BG2_button = obj_classes.Button("lava_button-modified (1).png", (850,180), scale = 1.1)
        game_selector_buttons = pygame.sprite.Group()
        game_selector_buttons.add(BG1_button, BG2_button)

        # Main Menu Graphics Loop
        while True:
            game_selected = False
            dt = clock.tick(data.frame_rate)
            for event in pygame.event.get():
                # Check if any event clicked button
                if BG1_button.update(event):
                    game_state = 1
                    game_selected = True
                    break # Breaks out of for loop
                if BG2_button.update(event):
                    game_state = 2
                    game_selected = True
                    break
                if event.type == pygame.QUIT:
                    sys.exit()
            if game_selected:
                break # breaks out of while loop
            screen.blit(image, (0,0))
            game_selector_buttons.draw(screen)
            pygame.display.flip()

    if game_state == 1 or game_state == 2: # Get Names
        # At the moment of clicking game-mode button, freeze present frame and blur it for background
        name_screen_freeze = screen.copy()
        name_screen_freeze = tools.blur_surface(name_screen_freeze, 2)
        # Load nameboard
        nameboard, nameboard_rect = tools.load_image("scoreboard.png", scale=0.5)
        nameboard_rect.center = data.nameboard_coords
        # Load Input
        player1_input = obj_classes.InputBox(1060, 400, 300, 70)
        player2_input = obj_classes.InputBox(1060, 600, 300, 70)
        submit_button = obj_classes.Button("submit-button.png", (960, 1000))
        inputs = [player1_input, player2_input]
        submitting_empty = False
        while True:
            dt = clock.tick(data.frame_rate)
            submit_clicked = False
            fair_submission = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                submit_clicked = submit_button.update(event)
                if submit_clicked:
                    # Checking if empty name given
                    if not player1_input.text or not player2_input.text:
                        submitting_empty = True 
                    else:
                        fair_submission = True
                for input_box in inputs:
                    input_box.handle_event(event) # If box is clicked, make its border blue to mimic selection
            
            for box in inputs:
                box.update() # Increases width if name is long
            if fair_submission:
                player1_name = player1_input.text
                player2_name = player2_input.text
                # Stops present BGM before moving to another game mode
                pygame.mixer.stop()
                break
            # Handle Graphics
            screen.blit(name_screen_freeze, (0,0))
            screen.blit(nameboard, nameboard_rect)
            screen.blit(submit_button.image, submit_button.rect)
            tools.load_font(screen, "Enter Names", pos = (960, 200), center=True, size=110)
            tools.load_font(screen, "Player 1: " , pos = (700,440), center=True)
            tools.load_font(screen, "Player 2: " , pos = (700,640), center=True)
            # Handle empty submission case
            if submitting_empty:
                tools.load_font(screen, "Name cannot be empty", pos = (960, 800), center=True)
                
            for box in inputs:
                box.draw(screen)
            
            pygame.display.flip()
    
    if game_state == 1: # Cradle of Wings
        pygame.mixer.music.load('sounds/Cradle_of_wings.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        while game_state == 1:
            game_state = engine_classes.BG1().run(player1_name, player2_name, screen)
        pygame.mixer.stop()
    
    if game_state == 2: # Molten Mayhem
        pygame.mixer.music.load('sounds/Molten_mayhem.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        while game_state == 2:
            game_state = engine_classes.BG1().run(player1_name, player2_name, screen, super=True)
        pygame.mixer.stop()


