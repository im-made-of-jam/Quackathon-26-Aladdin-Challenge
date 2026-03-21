import pygame # rendering library

from Images.InitImages import initImages
from Boxes.TextInputBox import TextInputBox
from Boxes.ListSelection import ListSelectionBox, ListSelectionItem
from Boxes.TextRenderBox import TextRenderBox
from Boxes.ClickableBox import ClickableBoxItem
from Boxes.ImageContainer import ImageContainer

# set up pygame for rendering
pygame.init()
screenSize = pygame.display.get_desktop_sizes()

if screenSize[0][0] == 2256 and screenSize[0][1] == 1504:
    quit()

# this is iwhere verything we draw goes
displaySurface = pygame.display.set_mode(screenSize[0], pygame.FULLSCREEN)

# this has every image in the ./Images/ folder
imageDict = initImages()

# all of the text boxes that will need to be drawn
textInputBoxes = [
    TextInputBox(x=700, y=100, w=300, h=50),  # income in the period
    TextInputBox(x=1050, y=100, w=300, h=50), # annual interest
    TextInputBox(x=300, y=500, w=300, h=50),  # money spent on food in the period
    TextInputBox(x=300, y=650, w=360, h=50),  # money spent on transport in the period
    TextInputBox(x=300, y=800, w=420, h=50),  # money spent on entertainment in the period
    TextInputBox(x=300, y=950, w=350, h=50),  # money spent on holidays in the period
    TextInputBox(x=800, y=500, w=420, h=50),  # money spent on anything else in the period
]
renderBoxes    = [
    TextRenderBox("Time period to calculate", x=300, y=40, w=360, h=50),
    TextRenderBox("Income in that time", x=700, y=40, w=300, h=50),
    TextRenderBox("Annual interest (%)", x=1050, y=40, w=300, h=50),
    TextRenderBox("Money spent on food", x=300, y=440, w=300, h=50),
    TextRenderBox("Money spent on transport", x=300, y=590, w=360, h=50),
    TextRenderBox("Money spent on entertainment", x=300, y=740, w=420, h=50),
    TextRenderBox("Money spent on holidays", x=300, y=890, w=350, h=50),
    TextRenderBox("Money spent on anything else", x=800, y=440, w=420, h=50),
]
imageContainers = [
    ImageContainer("logo", -10, 5),
    ImageContainer("pound_24x24", 680, 115), # income
    ImageContainer("pound_24x24", 280, 515), # food
    ImageContainer("pound_24x24", 280, 665), # transport
    ImageContainer("pound_24x24", 280, 815), # entertainment
    ImageContainer("pound_24x24", 280, 965), # holidays
    ImageContainer("pound_24x24", 780, 515), # anything else
]

listBoxes      = [
    ListSelectionBox(24, 300, 100),
]

listBoxes[0].addItem(ListSelectionItem("Weekly"   , 24, 0, 0  , 200, 50))
listBoxes[0].addItem(ListSelectionItem("Monthly"  , 24, 0, 50 , 200, 50))
listBoxes[0].addItem(ListSelectionItem("Quarterly", 24, 0, 100, 200, 50))
listBoxes[0].addItem(ListSelectionItem("Annually" , 24, 0, 150, 200, 50))

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

    # add any pictures we need draw
    for image in imageContainers:
        displaySurface.blit(imageDict[image.imageName], (image.x, image.y))

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

def calculateCashflow():
    def createSurface(string):
        ...

    income        = textInputBoxes[0].text # income in the period
    interest      = textInputBoxes[1].text # annual interest
    food          = textInputBoxes[2].text # money spent on food in the period
    transport     = textInputBoxes[3].text # money spent on transport in the period
    entertainment = textInputBoxes[4].text # money spent on entertainment in the period
    holidays      = textInputBoxes[5].text # money spent on holidays in the period

    if listBoxes[0].selectedItem is None:
        return createSurface("no time period selected")

    try:
        income = float(income)
    except ValueError:
        return createSurface("error in income box")

    try:
        interest = float(interest)
        interest /= 100
        interest += 1.0
    except ValueError:
        return createSurface("error in interest box")

    try:
        food = float(food)
    except ValueError:
        return createSurface("error in food box")

    try:
        transport = float(transport)
    except ValueError:
        return createSurface("error in transport box")

    try:
        entertainment = float(entertainment)
    except ValueError:
        return createSurface("error in entertainment box")

    try:
        holidays = float(holidays)
    except ValueError:
        return createSurface("error in holidays box")

# this has to go here so that calculateCashflow can access all of the previous boxes
clickableBoxes = [
    ClickableBoxItem("Calculate", 24, 1000, 800, 200, 50, callback=calculateCashflow),
]

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

                if ' ' == event.text:
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
