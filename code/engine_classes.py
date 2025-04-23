import obj_classes
import tools
import pygame
pygame.init()
import sys
import data
clock = pygame.Clock()
class BG1:
    def run(self, name1, name2, screen : pygame.Surface):
        image = pygame.image.load("images/background1.jpg")
        image = pygame.transform.scale_by(image,0.75)
        player1 = obj_classes.Player(name1, False)
        player2 = obj_classes.Player(name2, True)
        turn = False
        blocks = pygame.sprite.Group()
        blocks.add(player1.block_group, player2.block_group)
        print(player2.bird_group)
        while True:
            dt = clock.tick(data.frame_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()           
                if not turn:
                    player1.play(event)
                else:
                    #print("y")
                    player2.play(event)
            
            if not player2.bird_group and not player2.shot_bird and not player2.score_changing:
                break
            
            screen.blit(image, (0,0))
            turn = player1.update_shot_bird(dt, player2, turn, screen)
            turn = player2.update_shot_bird(dt, player1, turn, screen)
            
            blocks.update()

            #all_sprite.draw(screen)
            player1.draw(screen)
            player2.draw(screen)

            pygame.display.flip()
        game_end_freeze = screen.copy()
        game_end_freeze = tools.blur_surface(game_end_freeze, 2)
        scoreboard, scoreboard_rect = tools.load_image("scoreboard.png", scale=0.5)
        scoreboard_rect.center = data.scoreboard_coords 
        winner = player1 if player1.score > player2.score else player2
        exit_button = obj_classes.Button("exit_button.png", (960, 710))
        menu_button = obj_classes.Button("menu_button.png", (830, 710))
        replay_button = obj_classes.Button("replay_button.png", (1090, 710))
        buttons = pygame.sprite.Group()
        buttons.add(exit_button, menu_button, replay_button)
        while True:
            exit, menu, replay = False, False, False
            dt = clock.tick(data.frame_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()        
                exit = exit_button.update(event)
                menu = menu_button.update(event)
                replay = replay_button.update(event)
            if replay:
                return 1
            if menu:
                return 0
            if exit:
                sys.exit()
            screen.blit(game_end_freeze, (0,0))
            screen.blit(scoreboard, scoreboard_rect)
            tools.load_font(screen, f"{player1.name}:   {player1.score}", (960, 300), center=True)
            tools.load_font(screen, f"{player2.name}:   {player2.score}", (960, 400), center=True)
            tools.load_font(screen, f"{winner.name} WINS", pos=(960, 550), center=True, size=160)
            buttons.draw(screen)
            pygame.display.flip()



class BG2:
    def run(self, name1, name2, screen : pygame.Surface):
        image = pygame.image.load("images/BG2.jpeg")
        player1 = obj_classes.SuperPlayer(name1, False)
        player2 = obj_classes.SuperPlayer(name2, True)
        turn = False
        blocks = pygame.sprite.Group()
        blocks.add(player1.block_group, player2.block_group)
        print(player2.bird_group)
        while True:
            dt = clock.tick(data.frame_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()           
                if not turn:
                    player1.play(event)
                else:
                    #print("y")
                    player2.play(event)
            
            if not player2.bird_group and not player2.shot_bird and not player2.score_changing:
                break
            
            screen.blit(image, (0,0))
            turn = player1.update_shot_bird(dt, player2, turn, screen)
            turn = player2.update_shot_bird(dt, player1, turn, screen)
            
            blocks.update()

            #all_sprite.draw(screen)
            player1.draw(screen)
            player2.draw(screen)

            pygame.display.flip()
        game_end_freeze = screen.copy()
        game_end_freeze = tools.blur_surface(game_end_freeze, 2)
        scoreboard, scoreboard_rect = tools.load_image("scoreboard.png", scale=0.5)
        scoreboard_rect.center = data.scoreboard_coords 
        winner = player1 if player1.score > player2.score else player2
        exit_button = obj_classes.Button("exit_button.png", (960, 710))
        menu_button = obj_classes.Button("menu_button.png", (830, 710))
        replay_button = obj_classes.Button("replay_button.png", (1090, 710))
        buttons = pygame.sprite.Group()
        buttons.add(exit_button, menu_button, replay_button)
        while True:
            exit, menu, replay = False, False, False
            dt = clock.tick(data.frame_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()        
                exit = exit_button.update(event)
                menu = menu_button.update(event)
                replay = replay_button.update(event)
            if replay:
                return 1
            if menu:
                return 0
            if exit:
                sys.exit()
            screen.blit(game_end_freeze, (0,0))
            screen.blit(scoreboard, scoreboard_rect)
            tools.load_font(screen, f"{player1.name}:   {player1.score}", (960, 300), center=True)
            tools.load_font(screen, f"{player2.name}:   {player2.score}", (960, 400), center=True)
            tools.load_font(screen, f"{winner.name} WINS", pos=(960, 550), center=True, size=160)
            buttons.draw(screen)
            pygame.display.flip()



        


