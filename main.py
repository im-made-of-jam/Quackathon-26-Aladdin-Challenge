import pygame # rendering library

from InitImages import initImages

pygame.init()

screenSize = pygame.display.get_desktop_sizes()

displaySurface = pygame.display.set_mode(screenSize[0], pygame.FULLSCREEN)

imageDict = initImages()

def updateWindow():
    displaySurface.fill((255, 255, 255))

    displaySurface.blit(imageDict["obsidian"], ((screenSize[0][0] - imageDict["obsidian"].get_width()), 0))

    pygame.display.update()


while 1:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                quit()

            case pygame.KEYDOWN:
                if event.key == 27:
                    quit()

            case _:
                print(event)

    updateWindow()
