# Cian Linehan 119301381
# CS2513 Assignment 2

'''
The main extra functionality which I have added to this game is quick multiplication rounds. On multiples of 5 up to 20, there will be a bonus round. In each bonus round, you have 20 seconds to answer correctly for 2 points, if you take longer than this but are correct your score remains unchanged. If you are incorrect then regardless of time, you get -2 points. The points here are structured in such a way that you have to pass 4 of these bonus rounds to continue to the next part of the game. If you fail these bonus rounds 3 times, your score is reset to 0.
When the score is above 20 i.e. when you pass the 4th and final bonus round, the time which you have to press the squares halves to 1 second and you have to make it to 35 points to win. On reaching 35 points, the game ends and the time it took you to win is displayed on the screen in seconds.
Some other functionality includes a restart button which can be used except during bonus rounds to completely restart the game. Also, the squares randomly change colours. I have also handled the event in which a player does not input an integer for the multiplication rounds, in which I take it as the wrong answer and -2 points as before.
My idea for this game came from reaction time tests to test your reaction speed, this is why I included total time at the end. The game could easily be made harder by making the multiplication rounds harder or by decreasing the time allowed to press the squares even earlier. This makes it adaptable to the clients requests for difficulty.
'''
from tkinter import *
from random import *
from time import *


class Score:
    def __init__(self):
        self._score = 0

    def getScore(self):
        return self._score

    def addToScore(self, score):
        self._score = self._score + score

    def reset(self):
        self._score = 0

    def __str__(self):
        return 'Points: ' + str(self._score)

class Game:
    def __init__(self):
        self._main = Tk()
        self._main.title('Cian\'s Reaction Time Test')
        self._main.minsize(500,500)
        self._openCanvas()

        self._start = Button(self._main, text='Start', fg='blue', command=self._onStart, pady=5)
        self._start.grid(row=11,column=1)

        self._score = Score()
        self._scoreLabel = Label(self._main, text=self._score.__str__(), pady=20, fg='midnight blue')
        self._scoreLabel.config(font=("Arial Greek", 20))
        self._scoreLabel.grid(row=1,column=1)

        self._main.mainloop()

    def _openCanvas(self):
        self._canvas = Canvas(self._main, width=500, height=500)
        self._canvas.grid(row=2,column=1)


    def _onStart(self):
        self._failed = 0
        self._timeAllowed = 2
        self._countBonus = 0

        self._score.reset()
        self._scoreLabel['text'] = self._score.__str__()
        self._start['text'] = 'Restart'
        self._createRandom()
        self._startGameTime = time()

    def _createRandom(self):
        self._startTime = time()
        self._canvas.delete('all')

        xpos = randint(0,450)
        ypos = randint(0,450)
        randcolour = choice(['blue','yellow','red','green','black','orange','purple','pink','dim grey'])
        rect = self._canvas.create_rectangle(xpos, ypos, xpos+50, ypos+50, fill=randcolour)
        self._canvas.tag_bind(rect, '<ButtonPress-1>', self._onObjectClick)

    def _onObjectClick(self, event):
        elapsedTime = time() - self._startTime
        if elapsedTime <= self._timeAllowed:
            self._score.addToScore(1)
            self._scoreLabel['text'] = self._score.__str__()
            if self._score.getScore() % 5 == 0 and self._score.getScore() <= 20:
                self._bonusRound1()
            elif 20 < self._score.getScore() < 35:
                self._increaseSpeed()
            elif self._score.getScore() >= 35:
                self._win()
        self._createRandom()

    def _bonusRound1(self):

        self._start.grid_forget()
        self._countBonus += 1
        self._canvas.grid_forget()

        self._frame = Frame(self._main)
        self._frame.grid(row=3,column=1)

        self._startTime = time()
        global num1
        num1 = randint(0,15)
        global num2
        num2 = randint(0,25)

        global bonusLabel
        bonusLabel = Label(self._main, text='Quick multiplication bonus round {}!'.format(self._countBonus))
        bonusLabel.grid(row=2,column=1)
        bonusLabel.config(font=("Arial Greek", 14), fg='midnight blue')


        q = Label(self._frame, text='What is the product of {} x {}?'.format(str(num1),str(num2)), fg='red', font='italic')
        q.grid(row=1,column=1)

        self._answerBox = Entry(self._frame)
        self._answerBox.grid(row=3,column=2)

        l1 = Label(self._frame, text='Answer:' )
        l1.grid(row=3,column=1)

        l2 = Label(self._frame, text='You have 20 seconds! 2 points to play for.', fg='blue',bg='white' )
        l2.grid(row=2,column=1)

        global submit
        submit = Button(self._main, text='Submit',command=self._getAnswer,fg='blue')
        submit.grid(row=4,column=1)



    def _getAnswer(self):
        invalidInput = False
        try:
            answer = self._answerBox.get()
            int(answer)
        except:
            message = 'Invalid input, -2 points!'
            invalidInput = True
            self._score.addToScore(-2)

        elapsedTime = time() - self._startTime
        if not invalidInput:
            if int(num1 * num2) == int(answer):
                if elapsedTime <= 20:
                    message = 'You were on-time and correct, +2 points!'
                    self._score.addToScore(2)
                else:
                    message = 'You were correct but too slow, score remains unchanged!'

            else:
                message = 'Incorrect... the answer was {}, -2 points!'.format(str(num1 * num2))
                self._failed += 1
                if self._failed >= 3:
                    message = 'Incorrect... the answer was {}, -2 points! \nYou have failed 3 times! Your score will be reset.'.format(str(num1 * num2))
                    self._failed = 0
                    self._score.reset()
                else:
                    self._score.addToScore(-2)
        submit.grid_forget()
        self._scoreLabel['text'] = self._score.__str__()

        global l3
        l3 = Label(self._main, text=message, fg='black')
        l3.grid(row=8, column=1)
        global rejoin
        rejoin = Button(self._main, text='Rejoin main game', fg='blue', command=self._rejoinGame)
        rejoin.grid(row=9, column=1)


    def _rejoinGame(self):
        self._scoreLabel['text'] = self._score.__str__()
        self._start.grid(row=11, column=1)
        bonusLabel.grid_forget()
        self._frame.grid_forget()
        l3.grid_forget()
        rejoin.grid_forget()
        self._openCanvas()
        self._createRandom()

    def _increaseSpeed(self):
        self._scoreLabel['text'] += '\n\n Halving time allowed to press the squares..\n Make it to 35 points to win!'
        self._timeAllowed = 1

    def _win(self):
        self._start.grid_forget()
        self._canvas.grid_forget()
        endTime = round((time() - self._startGameTime), 4)
        self._scoreLabel['text'] = 'You have reached 35 points! Congratulations, you win.\n\nYour time was {} seconds.\n Try again to improve your reaction skills!'.format(endTime)


g=Game()
