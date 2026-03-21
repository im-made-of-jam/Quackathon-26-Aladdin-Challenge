import pygame # rendering library

from Images.InitImages import initImages
from Boxes.TextInputBox import TextInputBox
from Boxes.ListSelection import ListSelectionBox, ListSelectionItem
from Boxes.TextRenderBox import TextRenderBox
from Boxes.ClickableBox import ClickableBoxItem

# set up pygame for rendering
pygame.init()
screenSize = pygame.display.get_desktop_sizes()

# this is iwhere verything we draw goes
displaySurface = pygame.display.set_mode(screenSize[0], pygame.FULLSCREEN)

# this has every image in the ./Images/ folder
imageDict = initImages()

# all of the text boxes that will need to be drawn
textInputBoxes = []
listBoxes      = []
renderBoxes    = []
clickableBoxes = [ClickableBoxItem("Click Me!", 24, 1000, 100, 200, 50)]

# keep a track of the position of the mouse for highlighting various buttons
mousePos = [0, 0]

# keep a track of exit button globally so it still works when other things break
exitHovered = False

def updateWindow():
    """
    redraws the window and ultimately updates the screen
    """
    # make the background white
    displaySurface.fill((255, 255, 255))

    # add the obsidian logo
    displaySurface.blit(imageDict["logo"], (0, 0))

    # add the exit button
    if exitHovered:
        displaySurface.blit(imageDict["exit_light"], ((screenSize[0][0] - imageDict["exit_light"].get_width()), 0))
    else:
        displaySurface.blit(imageDict["exit"], ((screenSize[0][0] - imageDict["exit"].get_width()), 0))

    # make evry box update whether or not its hovered, then re-draw itself
    for box in textInputBoxes:
        box.updateHovered(mousePos)

        displaySurface.blit(box.render(), (box.x, box.y))

    for box in listBoxes:
        box.updateHovered(mousePos)

        displaySurface.blit(box.render(), (box.x, box.y))

    # these boxes dont have a hover or selection effect so just render them
    for box in renderBoxes:
        displaySurface.blit(box.render(), (box.x, box.y))

    for box in clickableBoxes:
        box.updateHovered(mousePos)

        displaySurface.blit(box.render(), (box.x, box.y))

    # update the screen
    pygame.display.update()

# main window loop
while 1:
    # keep a track of whether or not we actually had any events so we dont have to redraw the window if we dont need to
    haveHadEvent = False

    # process events as needed
    for event in pygame.event.get():
        haveHadEvent = True
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

                # update the look of the exit button
                if (event.pos[0] > (screenSize[0][0] - imageDict["exit"].get_width())) and (event.pos[1] < imageDict["exit"].get_height()):
                    exitHovered = True
                else:
                    exitHovered = False

            case pygame.MOUSEBUTTONDOWN:
                # quickly check for exit before doing any further processing
                if exitHovered:
                    quit()

                # make all boxes check to see if they are selected or not
                for box in textInputBoxes:
                    box.updateSelected()

                for box in listBoxes:
                    box.updateSelected()

                for box in clickableBoxes:
                    box.updateSelected()

            case _:
                pass

    if haveHadEvent:
        updateWindow()
