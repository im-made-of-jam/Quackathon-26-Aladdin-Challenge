import pygame # rendering library

from InitImages import initImages
from TextInputBox import TextInputBox

# set up pygame for rendering
pygame.init()
screenSize = pygame.display.get_desktop_sizes()

# this is iwhere verything we draw goes
displaySurface = pygame.display.set_mode(screenSize[0], pygame.FULLSCREEN)

# this has every image in the ./Images/ folder
imageDict = initImages()

# all of the text boxes that will need to be drawn
textInputBoxes = [TextInputBox(24, 10, 100, 100, 100)]

# keep a track of the position of the mouse for highlighting various buttons
mousePos = [0, 0]

def updateWindow():
    """
    redraws the window and ultimately updates the screen
    """
    # make the background white
    displaySurface.fill((255, 255, 255))

    # add the obsidian logo
    displaySurface.blit(imageDict["logo"], (0, 0))

    # add the exit button
    displaySurface.blit(imageDict["exit"], ((screenSize[0][0] - imageDict["exit"].get_width()), 0))

    for box in textInputBoxes:
        box.updateHovered(mousePos)

        displaySurface.blit(box.render(), (box.x, box.y))

    # update the screen
    pygame.display.update()

# main window loop
while 1:
    # process events as needed
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                quit()

            case pygame.TEXTINPUT:
                # type a number into a text box if possible
                if '0' <= event.text <= '9':
                    for box in textInputBoxes:
                        box.addIfSelected(event.text)

                # and the same for letters
                if 'a' <= event.text.lower() <= 'z':
                    for box in textInputBoxes:
                        box.addIfSelected(event.text)

            case pygame.KEYDOWN:
                # also handle backspace
                if event.key == 8:
                    for box in textInputBoxes:
                        box.addIfSelected(event.key)

            # update the position of the mouse
            case pygame.MOUSEMOTION:
                mousePos = [event.pos[0], event.pos[1]]

            case pygame.MOUSEBUTTONDOWN:
                # quickly check for exit before doing any further processing
                if (event.pos[0] > (screenSize[0][0] - imageDict["exit"].get_width())) and (event.pos[1] < imageDict["exit"].get_height()):
                    quit()

                # make all boxes check to see if they are selected or not
                for box in textInputBoxes:
                    box.updateSelected()

            case _:
                pass

    updateWindow()
