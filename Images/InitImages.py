import pygame

pygame.init()

def initImages() -> dict:
    """
    loads all of the images in the ./Images/ folder into a dict with the filename as the key, and a pygame surface as the value
    """
    import os

    returnDict = {}

    for filename in os.listdir("./Images"):
        returnDict[filename.split('.')[0]] = pygame.image.load("Images/"+filename)

    return returnDict
