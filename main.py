import pygame # rendering library

# to load images from disk
from Images.InitImages import initImages

# all the boxes for input
from Boxes.TextInputBox import TextInputBox
from Boxes.ListSelection import ListSelectionBox, ListSelectionItem
from Boxes.TextRenderBox import TextRenderBox
from Boxes.ClickableBox import ClickableBoxItem
from Boxes.ImageContainer import ImageContainer

# set up pygame for rendering
pygame.init()
screenSize = pygame.display.get_desktop_sizes()

# this is iwhere verything we draw goes
displaySurface = pygame.display.set_mode(screenSize[0], pygame.FULLSCREEN)

# this has every image in the ./Images/ folder
imageDict = initImages()

# all of the text boxes that will need to be drawn
textInputBoxes = [
    TextInputBox(x=700,  y=100, w=300, h=50),  # income in the period
    TextInputBox(x=1050, y=100, w=300, h=50),  # annual interest
    TextInputBox(x=300,  y=500, w=300, h=50),  # money spent on food in the period
    TextInputBox(x=300,  y=650, w=360, h=50),  # money spent on transport in the period
    TextInputBox(x=300,  y=800, w=420, h=50),  # money spent on entertainment in the period
    TextInputBox(x=300,  y=950, w=350, h=50),  # money spent on holidays in the period
    TextInputBox(x=800,  y=500, w=420, h=50),  # money spent on anything else in the period
]
renderBoxes    = [
    TextRenderBox("Time period to calculate",     x=300,  y=40,  w=360, h=50),
    TextRenderBox("Income in that time",          x=700,  y=40,  w=300, h=50),
    TextRenderBox("Annual interest (%)",          x=1050, y=40,  w=300, h=50),
    TextRenderBox("Money spent on food",          x=300,  y=440, w=300, h=50),
    TextRenderBox("Money spent on transport",     x=300,  y=590, w=360, h=50),
    TextRenderBox("Money spent on entertainment", x=300,  y=740, w=420, h=50),
    TextRenderBox("Money spent on holidays",      x=300,  y=890, w=350, h=50),
    TextRenderBox("Money spent on anything else", x=800,  y=440, w=420, h=50),
]
imageContainers = [
    ImageContainer("logo", -10, 5),
    ImageContainer("currencySymbol_24x24", 680,  115), # income
    ImageContainer("currencySymbol_24x24", 280,  515), # food
    ImageContainer("currencySymbol_24x24", 280,  665), # transport
    ImageContainer("currencySymbol_24x24", 280,  815), # entertainment
    ImageContainer("currencySymbol_24x24", 280,  965), # holidays
    ImageContainer("currencySymbol_24x24", 780,  515), # anything else
    ImageContainer("calculateResults",     1000, 650), # total income display box
    ImageContainer("calculateResults2",    1000, 710), # total outgoing display box
    ImageContainer("calculateResults3",    1000, 770), # total cashflow display box
    ImageContainer("calculateResults4",    1000, 830), # total interest display box
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
        if type(image) == pygame.surface.Surface:
            print(image)

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
    """
    calculate cashflow numbers and update the images that will be drawn to the screen
    """
    def createSurface(string):
        renderSurface = pygame.surface.Surface((600, 50))
        renderSurface.fill((255, 255, 255))

        # render the text kept within the box and draw it to the surface we will return
        renderSurface.blit(pygame.font.SysFont("mono", 24).render(string, True, (0, 0, 0)), (13, 13))

        return renderSurface

    income        = textInputBoxes[0].text # income in the period
    interest      = textInputBoxes[1].text # annual interest
    food          = textInputBoxes[2].text # money spent on food in the period
    transport     = textInputBoxes[3].text # money spent on transport in the period
    entertainment = textInputBoxes[4].text # money spent on entertainment in the period
    holidays      = textInputBoxes[5].text # money spent on holidays in the period
    misc          = textInputBoxes[6].text # money spent on anything else in the period

    if listBoxes[0].selectedItem is None:
        imageDict["calculateResults"] = createSurface("no time period selected")
        imageDict["calculateResults2"] = pygame.surface.Surface((1, 1))
        imageDict["calculateResults3"] = pygame.surface.Surface((1, 1))
        return

    try:
        income = float(income)
    except ValueError:
        imageDict["calculateResults"] = createSurface("error in income box")
        imageDict["calculateResults2"] = pygame.surface.Surface((1, 1))
        imageDict["calculateResults3"] = pygame.surface.Surface((1, 1))
        return

    try:
        interest = float(interest)
        interest /= 100
        interest += 1.0
    except ValueError:
        imageDict["calculateResults"] = createSurface("error in interest box")
        imageDict["calculateResults2"] = pygame.surface.Surface((1, 1))
        imageDict["calculateResults3"] = pygame.surface.Surface((1, 1))
        return

    try:
        food = float(food)
    except ValueError:
        imageDict["calculateResults"] = createSurface("error in food box")
        imageDict["calculateResults2"] = pygame.surface.Surface((1, 1))
        imageDict["calculateResults3"] = pygame.surface.Surface((1, 1))
        return

    try:
        transport = float(transport)
    except ValueError:
        imageDict["calculateResults"] = createSurface("error in transport box")
        imageDict["calculateResults2"] = pygame.surface.Surface((1, 1))
        imageDict["calculateResults3"] = pygame.surface.Surface((1, 1))
        return

    try:
        entertainment = float(entertainment)
    except ValueError:
        imageDict["calculateResults"] = createSurface("error in entertainment box")
        imageDict["calculateResults2"] = pygame.surface.Surface((1, 1))
        imageDict["calculateResults3"] = pygame.surface.Surface((1, 1))
        return

    try:
        holidays = float(holidays)
    except ValueError:
        imageDict["calculateResults"] = createSurface("error in holidays box")
        imageDict["calculateResults2"] = pygame.surface.Surface((1, 1))
        imageDict["calculateResults3"] = pygame.surface.Surface((1, 1))
        return

    try:
        misc = float(misc)
    except ValueError:
        imageDict["calculateResults"] = createSurface("error in anything else box")
        imageDict["calculateResults2"] = pygame.surface.Surface((1, 1))
        imageDict["calculateResults3"] = pygame.surface.Surface((1, 1))
        return

    # 365 days divided by this amount
    interestDivisor = 1 # one time per year by default

    match listBoxes[0].selectedItem.text:
        case "Weekly":
            interestDivisor = (365 / 7) # 52 and a bit times per year

        case "Monthly":
            interestDivisor = 12 # 12 times per year

        case "Quarterly":
            interestDivisor = 4 # 4 times per year

        case _:
            interestDivisor = 1 # ideally anually

    # the percent of interest for the period specified
    try:
        interestPerPeriod = interest ** (1 / interestDivisor)
    except ZeroDivisionError:
        interestPerPeriod = 0

    # a bunch of python black magic to turn it into a string with a decimal point
    totalIncomeSurface = pygame.surface.Surface((700, 50))
    totalIncomeSurface.fill((191, 191, 191))
    totalIncomePence = str(int(income * 100))
    totalIncomePence = totalIncomePence[:-2] + "." + totalIncomePence[-2:]

    # make sure there is always a leading zero
    if totalIncomePence[0] == ".":
        totalIncomePence = "0" + totalIncomePence

    # render the total income onto a surface that will be displayed
    totalIncomeSurface.blit(pygame.font.SysFont("mono", 24).render(("Total income for the period:  " + totalIncomePence), True, (0, 0, 0)), (13, 13))
    totalIncomeSurface.blit(imageDict["currencySymbol_24x24"], (412, 12))

    # replace the image in the dict with the surface we have just rendered
    imageDict["calculateResults"] = totalIncomeSurface

    # now do the same again but for total spending instead of total income
    totalSpending = food + transport + entertainment + holidays + misc

    totalSpendingSurface = pygame.surface.Surface((700, 50))

    totalSpendingSurface.fill((191, 191, 191))
    totalSpendingPence = str(int(totalSpending * 100))
    totalSpendingPence = totalSpendingPence[:-2] + "." + totalSpendingPence[-2:]

    if totalSpendingPence[0] == '.':
        totalSpendingPence = "0" + totalSpendingPence

    totalSpendingSurface.blit(pygame.font.SysFont("mono", 24).render(("Total spending for the period:  " + totalSpendingPence), True, (0, 0, 0)), (13, 13))
    totalSpendingSurface.blit(imageDict["currencySymbol_24x24"], (442, 12))

    imageDict["calculateResults2"] = totalSpendingSurface

    # now the same again but for total cashflow
    totalCashflowSurface = pygame.surface.Surface((700, 50))
    totalCashflowSurface.fill((191, 191, 191))
    totalCashflow = income - totalSpending
    totalCashflowPence = str(int(totalCashflow * 100))
    totalCashflowPence = totalCashflowPence[:-2] + "." + totalCashflowPence[-2:]

    if totalCashflowPence[0] == ".":
        totalCashflowPence = "0" + totalCashflowPence

    totalCashflowSurface.blit(pygame.font.SysFont("mono", 24).render(("Total cashflow for the period:  " + totalCashflowPence), True, (0, 0, 0)), (13, 13))
    totalCashflowSurface.blit(imageDict["currencySymbol_24x24"], (442, 12))

    imageDict["calculateResults3"] = totalCashflowSurface

    # calculate and display interest on the total cashflow
    totalInterestEarned = (interestPerPeriod * totalCashflow) - totalCashflow
    totalInterestEarnedSurface = pygame.surface.Surface((700, 50))
    totalInterestEarnedSurface.fill((191, 191, 191))
    totalInterestEarnedPence = str(int(totalInterestEarned * 100))
    totalInterestEarnedPence = totalInterestEarnedPence[:-2] + "." + totalInterestEarnedPence[-2:]

    if totalInterestEarnedPence[0] == ".":
        totalInterestEarnedPence = "0" + totalInterestEarnedPence

    if totalInterestEarned < 0:
        totalInterestEarnedSurface.blit(pygame.font.SysFont("mono", 24).render(("Total interest lost with this deficit:  " + totalInterestEarnedPence), True, (0, 0, 0)), (13, 13))
    else:
        totalInterestEarnedSurface.blit(pygame.font.SysFont("mono", 24).render(("Total interest earned with this money:  " + totalInterestEarnedPence), True, (0, 0, 0)), (13, 13))

    totalInterestEarnedSurface.blit(imageDict["currencySymbol_24x24"], (550, 12))

    imageDict["calculateResults4"] = totalInterestEarnedSurface

# this has to go here so that calculateCashflow can access all of the previous boxes
clickableBoxes = [
    ClickableBoxItem("Calculate", 24, 1000, 580, 200, 50, callback=calculateCashflow),
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

                if '.' == event.text:
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

            case pygame.VIDEOEXPOSE:
                updateWindow()

            case _:
                pass

    if haveHadEvent:
        updateWindow()
