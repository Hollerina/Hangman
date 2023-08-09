import tkinter as tk
import random
from tkinter import *
from PIL import ImageTk, Image

#create empty string for user input
word = ""
current = ""
counter = 1
found = 0
usedLets = ""
gInput = ""
wordDisplay = ""
wD = ""
used = ""
usedDisplay = ""

#create the window which will run the application/ the instance
window = tk.Tk()

#create all nine images
im1 = ImageTk.PhotoImage(Image.open("assets\\HM1.png"))
im2 = ImageTk.PhotoImage(Image.open("assets\\HM2.png"))
im3 = ImageTk.PhotoImage(Image.open("assets\\HM3.png"))
im4 = ImageTk.PhotoImage(Image.open("assets\\HM4.png"))
im5 = ImageTk.PhotoImage(Image.open("assets\\HM5.png"))
im6 = ImageTk.PhotoImage(Image.open("assets\\HM6.png"))
im7 = ImageTk.PhotoImage(Image.open("assets\\HM7.png"))
im8 = ImageTk.PhotoImage(Image.open("assets\\HM8.png"))
im9 = ImageTk.PhotoImage(Image.open("assets\\HM9.png"))

#The title of the game
title = tk.Label(text = "Hangman!")
title.pack()

#create the canvas where the image of the current state of hangman will be
#intial state will be blank while after every guess the state many be updated accordingly
canvas = Canvas(window,width = 300, height = 300)
canvas.pack()
cav = canvas.create_image(150,50, anchor = CENTER ,image = im1)

#Two player game mechanics
#get the first play to take the guess entry in
#uInput = tk.Entry(window)
#canvas.create_window(150,200, anchor = CENTER, window = uInput)

#Remove the orignal screen when getting user input
def delete():
    #get the user input
    global word
    word = uInput.get()
    canvas.delete("all")


#validate the User Input to be only one character or less
def callback(input):
    if len(input) <= 1:
        return True
    else:
        return False


#clearing the textbox entry. Guess button as well as enter key point here.
#When called will delete what was stored in the entry box. Due to guess being called first that value is captured first.
def clear_txt():
    gInput.delete(0, END)


#helper function for displaying the correct image of the hangman
def helper(value):
    if value == 2:
        canvas.itemconfig(cav, image = im2)
    elif value == 3:
        canvas.itemconfig(cav, image = im3)
    elif value == 4:
        canvas.itemconfig(cav, image = im4)
    elif value == 5:
        canvas.itemconfig(cav, image = im5)
    elif value == 6:
        canvas.itemconfig(cav, image = im6)
    elif value == 7:
        canvas.itemconfig(cav, image = im7)
    elif value == 8:
        canvas.itemconfig(cav, image = im8)
    elif value == 9:
        canvas.itemconfig(cav, image = im9)

#Restarting a game
def restart():
    canvas.delete("all")
    global cav
    cav = canvas.create_image(150,50, anchor = CENTER ,image = im1)
    global counter
    counter = 1
    global found
    found = 0
    global usedLets
    usedLets = ""
    beginGame()


#functions for winning and losing screen
def winner():
    canvas.delete("all")
    winMsg = tk.Label(text = "WINNER!")
    canvas.create_window(150,150, anchor = CENTER , window = winMsg)
    restartButton2 = tk.Button(text = "Restart", command = lambda : [restart()])
    canvas.create_window(150, 275, anchor = CENTER, window = restartButton2)

def loser():
    canvas.delete("all")
    canvas.create_image(150,100, anchor = CENTER ,image = im9)
    loseMsg = tk.Label(text = ("Loser the word was: " + word))
    canvas.create_window(150,200, anchor = CENTER , window = loseMsg)
    restartButton = tk.Button(text = "Restart", command = lambda : [restart()])
    canvas.create_window(150, 275, anchor = CENTER, window = restartButton)


#called to start the game
def beginGame():
    #cav = canvas.create_image(150,50, anchor = CENTER ,image = im1)

    #Get a random word
    with open("assets\\HMWords.txt", "r") as file:
        allText = file.read()
        words = list(map(str, allText.split()))

        #Grab a random word from the selection
        global word
        word = random.choice(words)
    
    #entry box for guesses and validation only one letter at a time
    global gInput
    gInput = tk.Entry(window)
    canvas.create_window(150, 150, anchor = CENTER, window = gInput)
    reg = window.register(callback)

    gInput.config(validate = "key", validatecommand = (reg, "%P"))

    #set the guessing word
    global current
    current =  "_  " * (len(word) - 1) + "_"
    global wordDisplay
    wordDisplay = tk.Label(text = current)
    global wD
    wD = canvas.create_window(150,237.5, anchor = CENTER, window = wordDisplay)

    #letters used
    global used
    used = tk.Label(text = "")
    global usedDisplay
    usedDisplay = canvas.create_window(150, 200, anchor = CENTER, window = used)

    #button for guessing
    button1 = tk.Button(text = "Guess", command = lambda : [guess(), clear_txt()])
    canvas.create_window(150,275, anchor = CENTER, window = button1)
    
    #bind the enter key buton to the guessing
    #lambda otherwise the function called would need an event argument
    window.bind("<Return>", lambda event: [guess(), clear_txt()])


#Guess will validate if the letter is the word being guessed
def guess():       
        guessValue = gInput.get().lower()
        global current
        if guessValue in word and guessValue not in current:
            #set a counter
            count = 0
            #Checking if more than one instance as well as where to update the ouput
            for element in word:
                if element == guessValue:
                    
                    current = current[:(count*3)] + element + current[(count * 3) + 1:]
                    global wordDisplay
                    wordDisplay = tk.Label(text = current)
                    canvas.itemconfig(wD, window = wordDisplay)
                    global found
                    found += 1
                count += 1
            if found == len(word):
                winner()                
        else:
            #update the image using a global counting
            global counter
            counter += 1

            #call the helper function to update the image
            helper(counter)

            #update the letter which was used
            global usedLets
            global used
            global usedDisplay
            #Don't want to add the letter more than once
            if guessValue not in usedLets:
                usedLets += guessValue + "  "
                used = tk.Label(text = usedLets)
                canvas.itemconfig(usedDisplay, window = used)
           
            if counter == 9:
                loser()
    
#start button for two player
#button = tk.Button(text = "Start", command = lambda: [delete(), beginGame()])
#canvas.create_window(150, 250, anchor = CENTER, window = button)

#begin the game
beginGame()

#allow for game to be ran 
window.mainloop()
