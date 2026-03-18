import os
import json
import quiz
import shutil
import pygame
import flashcards
import webbrowser
import GUIController
from datetime import timedelta

# Find path to chrome
chromePath = shutil.which("chrome") # windows path first as 2/3 of stakeholders mainly use windows devices

# chromepath is used to evaluate the condition as it can be truthy or falsy
# Truthy and Falsy are whether the value is null or not but can be used in
# Python to evaluate boolean statements despite not being explicit boolean types
if chromePath and os.path.exists(shutil.which("chrome")):
    chrome = webbrowser.BackgroundBrowser(shutil.which("chrome"))
else:
    chromePath = shutil.which("google-chrome")
    if chromePath and os.path.exists(shutil.which("google-chrome")):
        chrome = webbrowser.BackgroundBrowser(shutil.which("google-chrome"))
    elif os.path.exists("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
        chrome = webbrowser.BackgroundBrowser("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    else:
        print("COULD NOT FIND CHROME") # quick debug line

# Open just to read and debug what is in the file
# also makes sure file is closed properly
with open("usrSettings.json", "r") as file:
    settingsDict = json.load(file) # returns each object within the JSON as a dict

# dictionary for all flashcard sets
with open("flashcardSaves.json", "r") as file:
    flashDict = json.load(file)

# dictionary for the quiz questions
with open("quizSaves.json", "r") as file:
    quizDict = json.load(file)

#Initialise Buttons

#settings Buttons
settingsLabel = GUIController.Button(889, 30, GUIController.settingsTitleImg, 1)
toggleFullButton = GUIController.Button(654, 100, GUIController.toggleFullScreenImg, 1)

#home Buttons
openCalButton = GUIController.Button(1792, 0, GUIController.openCalImg, 0.0625)

#flashcard buttons
flashcardCorrectButton = GUIController.Button(500, 700, GUIController.flashcardCorrect, 1)
flashcardWrongButton = GUIController.Button(900, 700, GUIController.flashcardIncorrect, 1)
setButtons = []
cardIndex = 0

#revise Buttons
openQuizButton = GUIController.Button(396, 500, GUIController.openQuizModeImg, 1)
reviseModeLabel = GUIController.Button(699, 30, GUIController.reviseModeImg, 1)
openFlashcardsButton = GUIController.Button(50, 500, GUIController.openFlashcardsImg, 1)
openCheckpointButton = GUIController.Button(696, 500, GUIController.openCheckpointImg, 1)

#quiz test
#this is the main quiz mode, this is used twice so put into function
questionNum = 0
def runQuiz(quizDict):
    global questionNum
    quizBox = GUIController.Button(400, 200,GUIController.flashcardImg, 1.5)
    quizBox.draw()
    testQuestion = quiz.dictToQuiz(quizDict["testQuiz"]["questions"][questionNum], quizDict["testQuiz"]["topic"])
    testQuestion.options = quiz.dictToOption(testQuestion.options)
    testQuestion.displayQuestion()

    for option in testQuestion.options:
        if option.beenClickedOnce():
            if option.text != testQuestion.answer:
                option.isWrong()
            testQuestion.revealAnswer()
            questionNum +=1


#initialise MenuButtons
openReviseModeButton = GUIController.MenuButton(50, 413, GUIController.reviseModeImg, 1, [reviseModeLabel, openFlashcardsButton, openQuizButton])
openSettingsButton = GUIController.MenuButton(0,0,GUIController.settingsImg, 0.5, [toggleFullButton, settingsLabel])

running = True
calendarOpen = False

while running:
    GUIController.screen.fill((255,242,202))#lightyellow3 background
    currentScreen = settingsDict["startup"]["openScreen"]
    
    #return home
    if currentScreen == "home":
        GUIController.screen.blit(GUIController.titleImg, (895, 50))
        openSettingsButton.draw()
        openCalButton.draw()
        openReviseModeButton.draw()
        #rest of the homepage to be added here

        # check for buttons clicked on homepage
        if openReviseModeButton.beenClicked() and currentScreen != "reviseMode":
            settingsDict["startup"]["openScreen"] = "reviseMode"

        # open google calendar
        if openCalButton.beenClickedOnce() and not calendarOpen:
            chrome.open_new_tab("https://calendar.google.com")
            calendarOpen = True

        if openSettingsButton.beenClicked() and currentScreen != "settings":
            settingsDict["startup"]["openScreen"] = "settings"

    #keep the settings page open while 
    #currentScreen is set to settings page
    elif currentScreen == "settings":
        openSettingsButton.drawMenu()
        #rest of settings to go here

    elif currentScreen == "reviseMode":
        openReviseModeButton.drawMenu()
        # check for each button inside the revise mode menu
        if openFlashcardsButton.beenClickedOnce() and currentScreen != "flashcards":
            settingsDict["startup"]["openScreen"] = "chooseFlashSet"
        elif openQuizButton.beenClickedOnce() and currentScreen != "quiz":
            settingsDict["startup"]["openScreen"] = "quiz"
        elif openCheckpointButton.beenClickedOnce() and currentScreen != "checkpoint":
            settingsDict["startup"]["openScreen"] = "checkpoint"
        #add other revise mode buttons here

    #select flashcard set
    elif currentScreen == "chooseFlashSet":
        setButtons.clear()
        x = 100
        y = 200
        for setName in flashDict:
            button = GUIController.ButtonWithText(x, y, GUIController.flashcardImg, 0.3, setName)
            setButtons.append(button)
            # next FlashSet button is put 250 to the right
            x += 250
            # prevents buttons being drawn off screen 
            #by creating a new row
            if x > 1600:
                x = 100
                y += 200
        # put all FlashcardSet buttons on screen
        for button in setButtons:
            button.draw()
            if button.beenClickedOnce():
                flashSet = flashcards.loadSet(button.text)
                settingsDict["startup"]["openScreen"] = "flashcards"
                cardIndex = 0

        #flashcard mode
        if currentScreen == "flashcards":
            # If in range of array then display card at cardIndex
            if cardIndex < len(flashSet.cards):
                card = flashSet.cards[cardIndex]
                card.draw()
                #only check if card has been clicked 
                #if answer not revealed
                if not card.flipped:
                    if card.beenClickedOnce():
                        card.play()

                else: #card has now been flipped
                    flashcardCorrectButton.draw()
                    flashcardWrongButton.draw()
                    # If the user says they were correct
                    if flashcardCorrectButton.beenClickedOnce():
                        #change priority
                        card.correct += 1
                        card.updatePriority()
                        cardIndex += 1 # Move on and then save
                        flashcards.saveSet(flashSet, "testSet")
                    # If the user says they were wrong
                    elif flashcardWrongButton.beenClickedOnce():
                        #change priority  
                        card.wrong += 1
                        card.updatePriority()
                        cardIndex += 1 # Move on
                        flashcards.saveSet(flashSet, "testSet")
    
    #quiz mode
    elif currentScreen == "quiz":
        #do not check if this is clicked
        #this is just a box on screen
        runQuiz(quizDict)

    #a quiz with all of the weakest areas of the user 
    #will be a checkpoint
    elif currentScreen == "checkpoint":
        timesCorrect = quizDict["testQuiz"]["questions"][questionNum]["correct"]
        timesWrong = quizDict["testQuiz"]["questions"][questionNum]["wrong"]

        if timesCorrect != 0 or timesWrong != 0:
            successRate = timesCorrect / (timesCorrect + timesWrong)
        else:
            successRate = 0

        if successRate < 0.5:
            runQuiz(quizDict)

    # place this at end of checks
    # press esc to return home if not already
    keyPress = pygame.key.get_pressed()
    if keyPress[pygame.K_ESCAPE] and currentScreen != "home":
        settingsDict["startup"]["openScreen"] = "home"

# end of main loop

    # dump everything into the settings json
    with open("usrSettings.json", "w") as file:
        json.dump(settingsDict, file, indent=4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() # when quit pygame stop program

    pygame.display.update()