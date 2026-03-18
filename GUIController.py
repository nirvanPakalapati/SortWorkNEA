import pygame
import datetime
import eventCreator
from datetime import timedelta

pygame.init()
dimensions = pygame.display.get_desktop_sizes() # returns array of 1 tuple
screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption("SortWork")

# Initialise images to use throughout program
titleImg = pygame.image.load("assets/images/titleTag.png").convert_alpha()
createImg = pygame.image.load("assets/images/creationButton.png").convert_alpha()
openCalImg = pygame.image.load("assets/images/calendar_png").convert_alpha()
quizOptImg = pygame.image.load("assets/images/quizOptImg.png").convert_alpha()
settingsImg = pygame.image.load("assets/images/settings.png").convert_alpha()
flashcardImg = pygame.image.load("assets/images/baseFlashcard.png").convert_alpha()
reviseModeImg = pygame.image.load("assets/images/reviseModeImg.png").convert_alpha()
quizOptWrongImg = pygame.image.load("assets/images/quizOptWrong.png").convert_alpha()
openQuizModeImg = pygame.image.load("assets/images/quizMode.png").convert_alpha()
settingsTitleImg = pygame.image.load("assets/images/settingsTitle.png").convert_alpha()
flashcardCorrect = pygame.image.load("assets/images/cardCorrect.png").convert_alpha()
openFlashcardsImg = pygame.image.load("assets/images/openFlashcards.png").convert_alpha()
openCheckpointImg = pygame.image.load("assets/images/checkpoints.png").convert_alpha()
quizOptCorrectImg = pygame.image.load("assets/images/quizOptCorrect.png").convert_alpha()
flashcardIncorrect = pygame.image.load("assets/images/cardWrong.png").convert_alpha()
toggleFullScreenImg = pygame.image.load("assets/images/toggleFull.png").convert_alpha()

# Button class
class Button:
    def __init__(self, x, y, image, scale):
        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)

        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.wasMouseDown = False

    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)

    def beenClickedOnce(self):
        pos = pygame.mouse.get_pos()
        mouseDown = pygame.mouse.get_pressed()[0] # Check for left click
        clicked = False
        
        if self.rect.collidepoint(pos) and mouseDown and not self.wasMouseDown:
            clicked = True

        self.wasMouseDown = mouseDown
        return clicked

    def beenClicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            return True

# Only for buttons with static text
class ButtonWithText(Button):
    def __init__(self, x, y, image, scale, text):
        Button.__init__(self, x, y, image, scale)
        self.text = text
        self.backColour = (255, 255, 255)

    def draw(self):
        screen = pygame.display.get_surface()
        font = pygame.font.Font("freesansbold.ttf", 16)
        renderedText = font.render(self.text, True, (0, 0, 0), self.backColour)
        screen.blit(self.image, self.rect)
        screen.blit(renderedText, self.rect)

# These are buttons that will open menus
class MenuButton(Button):
    def __init__(self, x, y, image, scale, buttons):
        Button.__init__(self, x, y, image, scale)
        self.buttonList = buttons # array of Button objects

    def drawMenu(self):
        for button in self.buttonList:
            button.draw()
