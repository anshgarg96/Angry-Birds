import pygame
pygame.init()

# Directory for image assets
image_dir = "images/"

# Preload fonts for different sizes to avoid reloading repeatedly
font = {
    80 : pygame.font.Font("angrybirds-regular.ttf", 80),
    160 : pygame.font.Font("angrybirds-regular.ttf", 160),
    110 : pygame.font.Font("angrybirds-regular.ttf", 110)
}

def load_image(name, colorkey=None, scale=None, flip_x=False):
    """
    Loads and optionally scales/flips an image.

    name: File name of the image.
    colorkey: Transparency key. If -1, top-left pixel is used.
    scale: If provided, scales image by this factor.
    flip_x: If True, image is flipped horizontally
    """
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

def load_font(screen, text, pos, center=True, topleft=False, topright=False, size=80, wrap=0):
    """
    Renders and displays text onto the screen.

    screen (Surface): Target Pygame display surface.
    text (str): Text to be displayed.
    pos (tuple): Position for placement.
    center (bool): If True, center-aligns text.
    topleft (bool): If True, aligns to top-left.
    topright (bool): If True, aligns to top-right.
    size (int): Font size to use.
    wrap (int): Wrap length for long text.
    """
    text_surf = font[size].render(text, True, wraplength=wrap, color=(255,255,255))
    if center:
        text_surf_rect = text_surf.get_rect(center=pos)
    elif topleft:
        text_surf_rect = text_surf.get_rect(topleft=pos)
    elif topright:
        text_surf_rect = text_surf.get_rect(topright=pos)
    screen.blit(text_surf, text_surf_rect)

def disable_button(surface):
    """
    Converts an image to grayscale to visually disable a button.
        
    surface: The button surface to modify.

    Ref: https://stackoverflow.com/questions/17615963/standard-rgb-to-grayscale-conversion
    """
    arr = pygame.surfarray.pixels3d(surface)
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            r, g, b = arr[x, y]
            avg = (r + g + b) // 3
            arr[x, y] = (avg, avg, avg)
    del arr  # unlock the surface
    return surface

def blur_surface(surface, amount):
    """
    Applies a blur effect by downscaling and then upscaling the surface.

    surface: The surface to blur.
    amount: Intensity of the blur (higher means more blur).

    Ref: https://stackoverflow.com/questions/70006095/reducing-an-images-quality-by-downscaling-and-upscaling-to-create-pixelated-no
    """
    scale = 1.0 / amount
    size = surface.get_size()
    surf = pygame.transform.smoothscale(surface, (int(size[0] * scale), int(size[1] * scale)))
    return pygame.transform.smoothscale(surf, size)
