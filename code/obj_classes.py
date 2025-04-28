import pygame
import tools
import numpy as np
import random
import data
import time
sling_coords = [((500,730), (480, 730)), ( (1370, 730), (1390, 730))]
arming_pos_coords = [(520, 770), (1400,770)]
score_pos = [(50,50), (1870, 50)]
PowerUps_placeholder_coords = [
    [
        [80, 200],
        [80, 300],
        [80, 400]
    ],
    [
        [1840, 200],
        [1840, 300],
        [1840, 400]
    ]
]
bird_rest_placeholder_coords = [
    [
        (380,930),
        (310,930)
    ],
    [
        (1450, 930),
        (1520, 930)
    ]
]
block_coords = [
    [
        (30,700),
        (30,800),
        (140, 700),
        (140, 600),
        (250, 600),
        (250, 500),
        (360, 600)
    ],
    [
        (1820, 800),
        (1820, 700),
        (1710, 700),
        (1710, 600),
        (1600, 600),
        (1600, 500),
        (1490, 600)
    ]
]


class Player():
    def __init__(self, name, orientation, bird_arr, block_arr, ammo_arr : list, lava = False):
        self.super = False
        self.score_arr_index = 0
        self.score_changing = False
        self.score = 0
        self.new_score = 0
        self.name = name
        self.state = 0
        self.orientation = orientation
        self.initial_arming_pos = None
        self.final_arming_pos = None
        self.sling_stem = pygame.transform.flip(pygame.image.load(data.sling_image[0]), orientation, False)
        self.sling_other = pygame.transform.flip(pygame.image.load(data.sling_image[1]), orientation, False)
        self.sling_stem_rect = self.sling_stem.get_rect(topleft=sling_coords[orientation][0])
        self.sling_other_rect = self.sling_other.get_rect(topleft=sling_coords[orientation][1])
        self.bird_ammo = ammo_arr.copy()
        self.shot_bird = None
        self.initialise_bird_and_blocks(bird_arr, block_arr)
        self.birds_used = len(bird_rest_placeholder_coords) + 1
    
    def initialise_bird_and_blocks(self, bird_arr, block_arr):
        self.bird_group = pygame.sprite.Group()
        for idx, i in np.ndenumerate(bird_arr):
            self.bird_group.add(Bird(i, self.orientation))
        self.block_group = pygame.sprite.Group()
        for idx, i in np.ndenumerate(block_arr):
            self.block_group.add(Block(i))
        for i in range(data.number_of_blocks):
            self.block_group.sprites()[i].rect.x, self.block_group.sprites()[i].rect.y = block_coords[int(self.orientation)][i]
        
    def play(self, event):
        #print("==============================  STATE: ", self.state, "EVENT: ", event.type)
        if len(self.bird_group.sprites()) > 0:
            self.armed_bird = self.bird_group.sprites()[0]
        if self.state == 0:
            if event.type == pygame.MOUSEBUTTONUP:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.armed_bird.rect.collidepoint(mouse_pos):
                    self.state = 1
                    data.charge_sound.play()
                    self.initial_arming_pos = pygame.Vector2(mouse_pos)
        elif self.state == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.MOUSEBUTTONUP:
                self.start_time = time.time()
                data.shoot_sound.play()
                self.bird_group.remove(self.armed_bird)
                self.speed = self.calc_speed()
                if self.super:
                    self.wind_power.usage_status = False
                self.state = 2
                self.shot_bird = self.armed_bird
                if self.birds_used < data.number_of_birds:
                    self.bird_group.add(Bird(self.bird_ammo.pop(), self.orientation))
                    self.birds_used += 1
        elif self.state == 2:
            pass
    
    def update_shot_bird(self, dt, opponent, turn, screen, double_damage_power_factor = False, marker_limits = (470,1400)):
        if self.state == 1:
            self.simulated_path(screen, marker_limits= marker_limits)
        if len(self.bird_group.sprites()) > 0:
            self.bird_group.sprites()[0].rect.center= arming_pos_coords[int(self.orientation)]
        for i in range(1, len(self.bird_group.sprites())):
            self.bird_group.sprites()[i].rect.x, self.bird_group.sprites()[i].rect.bottom = bird_rest_placeholder_coords[int(self.orientation)][i-1]
        if not self.shot_bird:
            return turn
        else:
            self.shot_bird.rect.move_ip(int(self.speed[0]*(dt/1000)),int(self.speed[1]*(dt/1000)))
            self.speed[1] += data.gravity*dt
            collision_blocks = pygame.sprite.spritecollide(self.shot_bird, opponent.block_group, False)
            if collision_blocks:
                self.end_time = time.time()
                multiplier = 2 if double_damage_power_factor else 1
                for block in collision_blocks:
                    block.health = block.health - data.bird_dict[self.shot_bird.bird_type][block.block_type]*multiplier
                    self.new_score += data.bird_dict[self.shot_bird.bird_type][block.block_type]*multiplier*100
                self.new_score += int((self.end_time - self.start_time)*13)
                self.score_arr = np.linspace(self.score, self.new_score, data.frame_rate)
                self.score_changing = True
                self.shot_bird.kill()
                self.shot_bird = None
                self.state = 0
                return not turn
            if(self.shot_bird.rect.top < 0 or self.shot_bird.rect.bottom > 900 or self.shot_bird.rect.left < 0 or self.shot_bird.rect.right>1920):
                self.shot_bird.kill()
                self.shot_bird = None
                self.state = 0
                return not turn
            return turn
    
    def simulated_path(self, screen, marker_limits):
        speed = self.calc_speed()
        time_steps = 1/data.frame_rate
        marker = list(self.armed_bird.rect.center)
        count = 0
        total_count = 0
        while True:
            marker[0] += int(speed[0]*(time_steps))
            marker[1] += int(speed[1]*(time_steps))
            speed[1] += data.gravity*time_steps*1000
            if marker[1] < 0 or marker[1] > 900 or marker[0] < marker_limits[0] or marker[0]>marker_limits[1]:
                break
            count += 1
            total_count += 1
            if count==9:
                pygame.draw.circle(screen, (255, 0, 0), (int(marker[0]), int(marker[1])), 5)    
                count = 0

    def calc_speed(self, wind_advantage = 0):   
        self.final_arming_pos = pygame.Vector2(pygame.mouse.get_pos())
        projectile_speed_factor = min(170, self.final_arming_pos.distance_to(self.initial_arming_pos))
        projection_angle = ((self.initial_arming_pos - self.final_arming_pos).angle_to(pygame.Vector2(1, 0)))*np.pi/180
        speed = [np.cos(projection_angle)*projectile_speed_factor*data.base_speed + wind_advantage*(-1 if self.orientation else 1), np.sin(projection_angle)*projectile_speed_factor*data.base_speed*-1]
        return speed

    def draw(self, screen):
        if self.score_changing:
            display_score = int(self.score_arr[self.score_arr_index])
            if self.score_arr_index == data.frame_rate-1:
                self.score_arr_index = 0
                self.score_changing = 0
                if self.super:
                    i = 1
                    while self.new_score > i*500:
                        if self.score < i*500:
                            list = []
                            for x in self.PowerUps:
                                if not x.active_status:
                                    list.append(x)
                            print(list)
                            if list:
                                i = np.random.choice(np.arange(len(list)), 1)[0]
                                print(i)
                                list[i].active_status = True
                                self.PowerUps.update(pygame.event.Event(pygame.MOUSEBUTTONUP))
                            break
                        i += 1
                self.score = self.new_score
            self.score_arr_index += 1
        else:
            display_score = int(self.score)
        tools.load_font(screen, str(display_score), score_pos[self.orientation], center=False, topleft= (not self.orientation), topright = self.orientation)
        screen.blit(self.sling_stem, self.sling_stem_rect)
        self.bird_group.draw(screen)
        self.block_group.draw(screen)
        screen.blit(self.sling_other, self.sling_other_rect)
        if self.shot_bird:
            screen.blit(self.shot_bird.image, self.shot_bird.rect)


class SuperPlayer(Player):
    def __init__(self, name, orientation, bird_arr, block_arr, ammo_arr):
        super().__init__(name, orientation, bird_arr, block_arr, ammo_arr, lava=True)
        self.super = True
        self.PowerUps = pygame.sprite.Group()
        self.wind_power = PowerUps("wind_power_up.png", PowerUps_placeholder_coords[self.orientation][0])
        self.double_damage_power = PowerUps("double_damage_powerup.png", PowerUps_placeholder_coords[self.orientation][1])
        self.full_path_power = PowerUps("full_path.png", PowerUps_placeholder_coords[self.orientation][2])
        self.PowerUps.add(self.wind_power, self.double_damage_power, self.full_path_power)
        self.power_list = list(self.PowerUps)

        

    def play(self, event):
        if self.state == 0:
            self.PowerUps.update(event)
        super().play(event)

    def update_shot_bird(self, dt, opponent, turn, screen):
        marker_limits = (0,1920) if self.full_path_power.usage_status else (400,1470)
        x = super().update_shot_bird(dt, opponent, turn, screen, self.double_damage_power.usage_status, marker_limits)
        if self.score_changing and self.double_damage_power.usage_status:
            self.double_damage_power.usage_status = False
        if self.full_path_power.usage_status and self.state == 2:
            self.full_path_power.usage_status = False
        return x
    
    def calc_speed(self):
        if self.wind_power.usage_status:
            return super().calc_speed(data.wind_advantage)
        else:
            return super().calc_speed()
    
    def draw(self, screen):
        super().draw(screen)
        self.PowerUps.draw(screen)


class Bird(pygame.sprite.Sprite):
    def __init__(self, bird_type, orientation):
        super().__init__()
        self.bird_type = bird_type
        self.image, self.rect = tools.load_image(data.bird_dict[bird_type]["image_src"], flip_x=orientation)


class Block(pygame.sprite.Sprite):
    def __init__(self, block_type):
        super().__init__()
        self.block_type = block_type
        self.image, self.rect = tools.load_image(data.block_dict[block_type][3])
        self.health = 3

    def update(self):
        if self.health < 0:
            self.kill()
        else:
            self.image = tools.load_image(data.block_dict[self.block_type][self.health])[0]

class Button(pygame.sprite.Sprite):
    def __init__(self, button_img, button_pos, orientation = False, scale = 1.2):
        super().__init__()
        self.orientation = orientation
        self.button_img = button_img
        self.pos = button_pos
        self.image, self.rect = tools.load_image(button_img, flip_x=orientation)
        self.rect.center = button_pos
        self.hovering = False
        self.active_status = True
        self.scale = scale

    def update(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovering = True
            self.image, self.rect = tools.load_image(self.button_img, scale = self.scale, flip_x=self.orientation)
        else:
            self.hovering = False
            self.image, self.rect = tools.load_image(self.button_img, flip_x=self.orientation)
        self.rect.center = self.pos
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovering:
            return True
        return False
    
class PowerUps(Button):
    def __init__(self, button_img, button_pos, orientation = True):
        self.usage_status = False
        super().__init__(button_img, button_pos, orientation)

    def update(self, event):
        if self.active_status == True:
            x = super().update(event)
            if x:
                self.active_status = False
                self.usage_status = True
            return x
        else:
            self.image, self.rect = tools.load_image(self.button_img, flip_x=self.orientation)
            self.image = tools.disable_button(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        return False

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.base_width = w
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.border_color = self.color_inactive
        self.bg_color = pygame.Color('white')
        self.text_color = pygame.Color('black')
        self.text = text
        self.font = pygame.font.Font("angrybirds-regular.ttf", 80)
        self.txt_surface = self.font.render(text, True, self.text_color)
        self.active = False
        self.corner_radius = 10  # Change to your preferred roundness

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.border_color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.text_color)

    def update(self):
        width = max(self.base_width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Draw background with rounded corners
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.corner_radius)

        # Draw border with rounded corners
        pygame.draw.rect(screen, self.border_color, self.rect, width=5, border_radius=self.corner_radius)

        # Draw text
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y - 12))
        

