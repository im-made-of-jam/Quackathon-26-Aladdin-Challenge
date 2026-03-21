import pygame

pygame.init()

def initImages() -> dict:
    import os

    returnDict = {}

    for filename in os.listdir("./Images"):
        returnDict[filename.split('.')[0]] = pygame.image.load("Images/"+filename)

    return returnDict

initImages()
