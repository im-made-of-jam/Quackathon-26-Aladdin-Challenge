import pygame

textRenderBoxHoveredBackground    = (191, 191, 191)

class TextRenderBox:
    # x and y position of the top left of the box
    # w and h for width and height of the box
    def __init__(self, text="", fontSize=24, x=0, y=0, w=0, h=0, fontName="mono"):
        self.text = text
        self.fontSize = fontSize
        self.fontName = fontName

        # position and size of the box
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # information about selection
        self.isHovered = False
        self.isSelected = False

    # draw self, and return it as a pygame surface ready for blitting
    def render(self) -> pygame.surface.Surface:
        # make the surface and fill it with the appropriate background colour
        renderSurface = pygame.surface.Surface((self.w, self.h))

        renderSurface.fill(textRenderBoxHoveredBackground)

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
