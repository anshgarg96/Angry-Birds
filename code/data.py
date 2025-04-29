import pygame
charge_sound = pygame.mixer.Sound("sounds/charge.mp3")
charge_sound.set_volume(0.8)
shoot_sound = pygame.mixer.Sound("sounds/shoot.mp3")
shoot_sound.set_volume(0.5)
frame_rate = 50
no_of_markers = 10
gravity = 0.5
base_speed = 5.5
wind_advantage = 1000
bird_dict = {
    "red" : {
        "image_src" : "red.png",
        "wood" : 1,
        "stone" : 1,
        "ice" : 1,
        "wood-lava" : 1,
        "stone-lava" : 1,
        "ice-lava" : 1
    },
    "chuck":{
        "image_src" : "chuck.png",
        "wood" : 2,
        "stone" : 1,
        "ice" : 1,
        "wood-lava" : 2,
        "stone-lava" : 1,
        "ice-lava" : 1
    },
    "bomb":{
        "image_src" : "bomb.png",
        "wood" : 1,
        "stone" : 2,
        "ice" : 1,
        "wood-lava" : 1,
        "stone-lava" : 2,
        "ice-lava" : 1
    },
    "blues":{
        "image_src" : "blues.png",
        "wood" : 1,
        "stone" : 1,
        "ice" : 2,
        "wood-lava" : 1,
        "stone-lava" : 1,
        "ice-lava" : 2
    }
}
number_of_birds = 10
block_dict = {
    "wood" : {
        0 : "wood-square-0.png",
        1 : "wood-square-1.png",
        2 : "wood-square-2.png",
        3 : "wood-square-3.png",
    },
    "stone" : {
        0 : "stone-square-0.png",
        1 : "stone-square-1.png",
        2 : "stone-square-2.png",
        3 : "stone-square-3.png",
    },
    "ice" : {
        0 : "ice-square-0.png",
        1 : "ice-square-1.png",
        2 : "ice-square-2.png",
        3 : "ice-square-3.png",
    },
    "wood-lava" : {
        0 : "lava_wood_0.png",
        1 : "lava_wood_1.png",
        2 : "lava_wood_2.png",
        3 : "lava_wood_3.png",
    },
    "stone-lava" : {
        0 : "lava_stone_0.png",
        1 : "lava_stone_1.png",
        2 : "lava_stone_2.png",
        3 : "lava_stone_3.png",
    },
    "ice-lava" : {
        0 : "lava_ice_0.png",
        1 : "lava_ice_1.png",
        2 : "lava_ice_2.png",
        3 : "lava_ice_3.png",
    }


}
number_of_blocks = 7
sling_image = ["images/sling_stem.png", "images/sling_other.png"]
scoreboard_coords = (960, 500)
nameboard_coords = (960, 500)