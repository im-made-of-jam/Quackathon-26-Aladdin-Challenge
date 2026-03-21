import pygame

textInputBoxSelectedBackground   = (255, 255, 255)
textInputBoxHoveredBackground    = (191, 191, 191)
textInputBoxDeSelectedBackground = (127, 127, 127)

class TextInputBox:
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

        # information about selection
        self.isHovered = False
        self.isSelected = False

    # add a letter to self, unless its backspace, and only if this box is currently selected
    def addIfSelected(self, letter: str | int) -> None:
        if not self.isSelected:
            return

        if type(letter) == int:
            if self.text:
                self.text = self.text[:-1]
            return

        else:
            self.text += letter

    # check to see if the mouse if hovering over this box or not
    def updateHovered(self, mousePos) -> None:
        self.isHovered = False

        if (mousePos[0] >= self.x) and (mousePos[0] <= (self.x + self.w)):
            # mouse is aligned horizontally
            if (mousePos[1] >= self.y) and (mousePos[1] <= (self.y + self.h)):
                # mouse is also aligned vertically
                self.isHovered = True

    # this should be called when the mouse is clicked, *after* updateHovered
    def updateSelected(self):
        self.isSelected = self.isHovered

    # draw self, and return it as a pygame surface ready for blitting
    def render(self) -> pygame.surface.Surface:
        # make the surface and fill it with the appropriate background colour
        renderSurface = pygame.surface.Surface((self.w, self.h))
        if self.isSelected:
            renderSurface.fill(textInputBoxSelectedBackground)

        elif self.isHovered:
            renderSurface.fill(textInputBoxHoveredBackground)

        else:
            renderSurface.fill(textInputBoxDeSelectedBackground)

        # use the same position for X and Y within the box because it looks nice
        position = (self.h / 2) - (self.fontSize / 2)

        # render the text kept within the box and draw it to the surface we will return
        renderSurface.blit(pygame.font.SysFont(self.fontName, self.fontSize).render(self.text, True, (0, 0, 0)), (position, position))

        return renderSurface
