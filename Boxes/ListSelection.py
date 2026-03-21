import pygame

listSelectionItemSelectedColour   = (255, 255, 255)
listSelectionItemHoveredColour    = (191, 191, 191)
listSelectionItemDeselectedColour = (127, 127, 127)

# an item that can be selected in a list
class ListSelectionItem:
    # x and y position of the top left of the box
    # w and h for width and height of the box
    # *** BOTH OF THESE ARE RELATIVE TO THE PARENT BOX ***
    def __init__(self, text="", fontSize=24, x=0, y=0, w=0, h=0, fontName="mono"):
        self.text = text
        self.fontSize = fontSize
        self.fontName = fontName

        # position and size of the box
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.isHovered = False
        self.isSelected = False

    # check to see if the mouse if hovering over this box or not
    # *** MOUSE POSITIONED RELATIVE TO THE LIST ***
    def updateHovered(self, mousePos) -> None:
        self.isHovered = False

        if (mousePos[0] >= self.x) and (mousePos[0] <= (self.x + self.w)):
            # mouse is aligned horizontally
            if (mousePos[1] >= self.y) and (mousePos[1] <= (self.y + self.h)):
                # mouse is also aligned vertically
                self.isHovered = True

    # this should be called when the mouse is clicked, *after* updateHovered
    # returns True if the item should be selected, False otherwise
    def checkSelected(self):
        return self.isHovered

    # draw self, and return it as a pygame surface ready for blitting
    def render(self, selectedItem) -> pygame.surface.Surface:
        # make the surface and fill it with the appropriate background colour
        renderSurface = pygame.surface.Surface((self.w, self.h))
        if self is selectedItem:
            renderSurface.fill(listSelectionItemSelectedColour)

        elif self.isHovered:
            renderSurface.fill(listSelectionItemHoveredColour)

        else:
            renderSurface.fill(listSelectionItemDeselectedColour)

        # use the same position for X and Y within the box because it looks nice
        position = (self.h / 2) - (self.fontSize / 2)

        # render the text kept within the box and draw it to the surface we will return
        renderSurface.blit(pygame.font.SysFont(self.fontName, self.fontSize).render(self.text, True, (0, 0, 0)), (position, position))

        # render the outline of the box
        pygame.draw.line(renderSurface, (0, 0, 0), (0, 0), ((self.w - 1), 0)                      , 5) # top
        pygame.draw.line(renderSurface, (0, 0, 0), ((self.w - 1), 0), ((self.w - 1), (self.h - 1)), 5) # right
        pygame.draw.line(renderSurface, (0, 0, 0), (0, (self.h - 1)), ((self.w - 1), (self.h - 1)), 5) # bottom
        pygame.draw.line(renderSurface, (0, 0, 0), (0, 0), (0, (self.h - 1))                      , 5) # left

        return renderSurface


class ListSelectionBox:
    # x and y position of the top left of the box
    # w and h for width and height of the box
    def __init__(self, fontSize=24, x=0, y=0, w=0, h=0, fontName="mono"):
        self.text = ""
        self.fontSize = fontSize
        self.fontName = fontName

        # positoin and size of the box
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.allItems = []

        self.selectedItem = None

        self.size = None

    # update whether or not an item in the list has been selected
    def updateSelected(self):
        for item in self.allItems:
            if item.checkSelected():
                self.selectedItem = item

    # update whether or not the mouse is hovering over this list
    def updateHovered(self, mousePos):
        for item in self.allItems:
            item.updateHovered(((mousePos[0] - self.x), (mousePos[1] - self.y)))

    # render this list
    def render(self):
        # if we dont know how big the list is then go and update that
        if self.size == None:
            self.updateSize()

        # create the surface to render to and fill it in with black. this makes a nice border between elements too
        renderSurface = pygame.surface.Surface((self.size[0], self.size[1]))
        renderSurface.fill((0, 0, 0))

        # draw every item in the list to the surface we will return
        for item in self.allItems:
            renderSurface.blit(item.render(self.selectedItem), (item.x, item.y))

        return renderSurface

    # update the maximum size of this list item
    def updateSize(self):
            # need to find the maximum size of any item in the list for both x and y
            maxX = 0
            maxY = 0

            for item in self.allItems:
                rightSide = item.x + item.w

                if rightSide > maxX:
                    maxX = rightSide

                bottom = item.y + item.h

                if rightSide > maxY:
                    maxY = bottom

            self.size = (maxX, maxY)

    def addItem(self, item):
        self.allItems.append(item)
        self.updateSize()
