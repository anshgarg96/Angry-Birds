import obj_classes
import tools
import pygame
import numpy as np
pygame.init()
import sys
import data
clock = pygame.Clock()
class BG1:
    def run(self, name1, name2, screen : pygame.Surface, super = False):
        """
        super : Flag for superplayer, if True modifies certain parts of code 
        """
        
        # Tells it which indices of data.block_dict to cover according to game-mode
        block_dict_start_index = 3 if super else 0
        block_dict_stop_index = 6 if super else 3
        
        # Generate block and bird arrays randomly
        bird_arr = np.random.choice( np.array(list(data.bird_dict.keys())), min(data.number_of_birds, len(obj_classes.bird_rest_placeholder_coords) + 1), True)
        block_arr = np.random.choice( np.array(list(data.block_dict.keys())[block_dict_start_index:block_dict_stop_index]), data.number_of_blocks, True)
        if data.number_of_birds > len(obj_classes.bird_rest_placeholder_coords) + 1:
            ammo_arr = list(np.random.choice( np.array(list(data.bird_dict.keys())), data.number_of_birds - len(obj_classes.bird_rest_placeholder_coords) + 1, True))
        
        # Initialise Player or SuperPlayer depending upon super flag
        if not super:
            player1 = obj_classes.Player(name1,  False, bird_arr, block_arr, ammo_arr)
            player2 = obj_classes.Player(name2, True, bird_arr, block_arr, ammo_arr)
            image = pygame.image.load("images/background1.jpg")
            image = pygame.transform.scale_by(image,0.75)
        else:
            image = pygame.image.load("images/BG2.jpeg")
            player1 = obj_classes.SuperPlayer(name1, False, bird_arr, block_arr, ammo_arr)
            player2 = obj_classes.SuperPlayer(name2, True, bird_arr, block_arr, ammo_arr)

        turn = False # Primary variable for handling player turn
        blocks = pygame.sprite.Group()
        blocks.add(player1.block_group, player2.block_group)

        # Game Loop
        while True:
            dt = clock.tick(data.frame_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()           
                # Handling Player's state depending on whose turn it is
                if not turn:
                    player1.play(event)
                else:
                    player2.play(event)
            
            # Winning conditions
            if not player2.bird_group and not player2.shot_bird and not player2.score_changing: # All birds exhausted
                break
            if not player1.block_group or not player2.block_group: # someone's tower broken
                break
            
            screen.blit(image, (0,0))
            # Handle bird flying, collision and score change, return (turn) or (not turn) depending upon what is going on currently
            turn = player1.update_shot_bird(dt, player2, turn, screen)
            turn = player2.update_shot_bird(dt, player1, turn, screen)
            
            # Handle block image according to health
            blocks.update()

            # Draw each player's sprites
            player1.draw(screen)
            player2.draw(screen)

            pygame.display.flip()
        game_end_freeze = screen.copy()
        game_end_freeze = tools.blur_surface(game_end_freeze, 2)
        scoreboard, scoreboard_rect = tools.load_image("scoreboard.png", scale=0.5)
        scoreboard_rect.center = data.scoreboard_coords

        # Check for tie
        TIE = player1.score == player2.score
        if not TIE:
            winner = player1 if player1.score > player2.score else player2 # Determine Winner
        # Post-game Buttons 
        exit_button = obj_classes.Button("exit_button.png", (960, 710))
        menu_button = obj_classes.Button("menu_button.png", (830, 710))
        replay_button = obj_classes.Button("replay_button.png", (1090, 710))
        buttons = pygame.sprite.Group()
        buttons.add(exit_button, menu_button, replay_button)
        # Winning Screen Loop
        while True:
            exit, menu, replay = False, False, False
            dt = clock.tick(data.frame_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()        
                exit = exit_button.update(event)
                menu = menu_button.update(event)
                replay = replay_button.update(event)
            # Return next Game-state value
            if replay:
                return 1
            if menu:
                return 0
            if exit:
                sys.exit()
            screen.blit(game_end_freeze, (0,0))
            screen.blit(scoreboard, scoreboard_rect)

            # Display Score and Winner
            tools.load_font(screen, f"{player1.name}:   {player1.score}", (960, 300), center=True)
            tools.load_font(screen, f"{player2.name}:   {player2.score}", (960, 400), center=True)
            if not TIE:
                tools.load_font(screen, f"{winner.name} WINS", pos=(960, 550), center=True, size=160)
            else:
                tools.load_font(screen, "DRAW", pos=(960, 550), center=True, size=160)
            buttons.draw(screen)
            pygame.display.flip()



        


