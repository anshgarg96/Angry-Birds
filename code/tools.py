import pygame
pygame.init()
image_dir = "images/"

font = {
    80 : pygame.font.Font("angrybirds-regular.ttf", 80),
    160 : pygame.font.Font("angrybirds-regular.ttf", 160),
    110 : pygame.font.Font("angrybirds-regular.ttf", 110)
}

def load_image(name,colorkey = None, scale = None, flip_x = False):
    image = pygame.image.load(f"{image_dir}{name}")
    if scale:
        image = pygame.transform.smoothscale_by(image, scale)

    if flip_x:
        image = pygame.transform.flip(image, True, False)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

def load_font(screen, text, pos, center = True, topleft = False, topright = False, size = 80, wrap = 0):
    text_surf = font[size].render(text, True, wraplength=wrap, color=(255,255,255))
    if center:
        text_surf_rect = text_surf.get_rect(center = pos)
    if topleft:
        text_surf_rect = text_surf.get_rect(topleft = pos)
    if topright:
        text_surf_rect = text_surf.get_rect(topright = pos) 
    
    screen.blit(text_surf, text_surf_rect)

def disable_button(surface):
    arr = pygame.surfarray.pixels3d(surface)
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            r, g, b = arr[x, y]
            avg = (r + g + b) // 3
            arr[x, y] = (avg, avg, avg)
    del arr  # unlock the surface
    return surface

def blur_surface(surface, amount):
    scale = 1.0 / amount
    size = surface.get_size()
    surf = pygame.transform.smoothscale(surface, (int(size[0] * scale), int(size[1] * scale)))
    return pygame.transform.smoothscale(surf, size)

    


