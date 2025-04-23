import sys, pygame
pygame.init()
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
screen = pygame.display.set_mode((1920,1080))
image = pygame.image.load("images/background1.jpg")
image = pygame.transform.scale_by(image,0.75)
screen.blit(image, (0,0))
block = pygame.image.load("images/wood-square-3.png")
screen.blit(block, (0, 850))
bird = pygame.image.load("images/red-bird.png")
screen.blit(bird, (200, 850))
screen.blit(bird, (100, 850))
screen.blit(bird, (1570, 850))
image1 = pygame.image.load("images/sling.png")
screen.blit(image1, (350,730))
image2 = pygame.image.load("images/sling.png")
image2 = pygame.transform.flip(image2, True, False)
screen.blit(image2, (1570-image2.get_size()[0],730))

print(image2.get_size()[0])
#displayInfo = pygame.display.Info()
#print(displayInfo.current_w, displayInfo.current_h)
while True:
    if pygame.QUIT in pygame.event.get():
        sys.exit() 
    pygame.display.flip()