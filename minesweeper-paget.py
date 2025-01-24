import tkinter as tk
from tkinter import font as tkFont
import random


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.titlefont = tkFont.Font(family="Arial", size=20, slant="italic")
        self.buttonFont = tkFont.Font(family="Arial", size=18)
        self.label = tk.Label(self, text="Minesweeper", font=self.titlefont)
        self.label.grid(row=0, column=1)
        self.goButton = tk.Button(self, text="    Go!    ", command=self.go, bg="green", fg="white")
        self.goButton.grid(row=0, column=0)
        self.buttongrid = tk.Frame(self)
        self.buttongrid.grid(row=2, column=0, sticky="NSEW", columnspan=2)
        self.buttons = []
        self.flagImage = tk.PhotoImage(file="flag.gif")
        self.mineImage = tk.PhotoImage(file="mine.gif")
        self.nomineImage = tk.PhotoImage(file="nomine.gif")
        buttonNum = 0
        for rownum in range(10):
            for columnnum in range(10):
                self.buttons.append(tk.Button(self.buttongrid, text=" ", font=self.titlefont))
                self.buttons[buttonNum].bind("<Button-1>", lambda event, x=buttonNum: self.buttonLeftClicked(event, x))
                self.buttons[buttonNum].bind("<Button-3>", lambda event, x=buttonNum: self.buttonRightClicked(event, x))
                self.buttons[buttonNum].config(height=50, width=50)
                self.buttons[-1].grid(row=rownum, column=columnnum, sticky="NSEW")
                self.buttongrid.rowconfigure(rownum, weight=1)
                self.buttongrid.columnconfigure(columnnum, weight=1)
                buttonNum += 1
        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)
        self.go()

    def buttonLeftClicked(self, event, pos):
        if self.gameOn:
            print("Button", pos, " was left clicked")
            if self.minepositions[pos] == 1:
                self.dead()
            else:
                self.floodfill(pos)



    def checkWin(self):
        win = True
        for pos in range(100):
            # if this is flagged and there is not a mine here, win = false
            if self.buttons[pos].cget("image") == "pyimage1" and self.minepositions[pos] == 0:  
                win = False
            # if this is a mine and it's not flagged, win = false
            if self.buttons[pos].cget("image") != "pyimage1" and self.minepositions[pos] == 1:  
                win = False
        return win
        
        
    def buttonRightClicked(self, event, num):
        # when right clicked, a mine will either show a flag or hide the flag
        if self.gameOn:
            if self.buttons[num].cget("image") == "pyimage1":
                self.buttons[num].config(image="")
            else:
                self.buttons[num].config(image=self.flagImage)
            
        if self.checkWin():	
            for pos in range(100):
                self.buttons[pos].config(text="WIN", bg="green")
                self.gameOn=False

    def placeMines(self):
        self.minepositions = [0 for x in range(100)]
        # self.minepositions is a 100-slot array containing 0 for blank cells and 1 for mines
        # 20 mines should be placed randomly
        
        minecount = 0
        while minecount < 20:
            num = random.randint(0,99)
            if self.minepositions[num] == 0:
                self.minepositions[num] = 1
                #self.buttons[num].config(text="X")
                minecount+=1



    def getNoMines(self, pos):
        numberMines = 0
        # this checks the neighbouring cells of postion pos and counts the number of mines
        # it returns the number
        column = pos % 10
        
        if pos > 9: # if not on the top row, look up
            numberMines = numberMines + self.minepositions[pos-10]
        if pos < 90: # if not on the bottom row, look down
            numberMines = numberMines + self.minepositions[pos+10]
        if column > 0: # if not in left column, look left
            numberMines = numberMines + self.minepositions[pos-1]
        if column < 9: # if not in right column, look right
            numberMines = numberMines + self.minepositions[pos+1]
        if column > 0 and pos > 9: # looking up left
            numberMines = numberMines + self.minepositions[pos-11]
        if column <9  and pos > 9: # looking up and right
            numberMines = numberMines + self.minepositions[pos-9]
        if column > 0 and pos < 90: # down and left
            numberMines = numberMines + self.minepositions[pos+9]
        if column < 9 and pos < 90: # down and right
            numberMines = numberMines + self.minepositions[pos+11]
        return numberMines

    def dead(self):
        self.gameOn = False
        # This changes all the cells to red, reveals the mines and ends the game
        for pos in range(100):
        # To change the image on a button to a mine, use this:
            if self.minepositions[pos] == 1:
                self.buttons[pos].config(image=self.mineImage)

        # To change the colour and style of button:
            self.buttons[pos].config(state="normal", bg="red", relief="raised")

    def floodfill(self, pos):
        # This reveals all the contiguous blank spaces in a flood-fill manner.
        # so all the blank cells are revealed, and a 'border' of mine numbers around the area are also revealed

        # To make a button appear flat:
        # self.buttons[pos].config(image="", state="disabled", relief="flat", bg="lightblue")

        q = [pos]
        visited=[ ]

        while len(q) >0:
            # pop the first item from the queue
            thispos = q.pop(0)
            visited.append(thispos)
            # find out how many neighbouring mines it has
            mines = self.getNoMines(thispos)
            # if it's a number > 0: put the number on this button
            if mines > 0:
                self.buttons[thispos].config(text=mines)
            # if its zero, add all of its neighbors into the queue
            else:
                self.buttons[thispos].config(image="", state="disabled", relief="flat", bg="lightblue")
                column = thispos % 10
                
                if thispos > 9 and column > 0 and thispos-11 not in visited and thispos-11 not in q:  # looking up and left
                    q.append(thispos-11)
                    
                if thispos > 9 and thispos-10 not in visited and thispos-10 not in q:                 # looking up
                    q.append(thispos-10)
                    
                if thispos > 9 and column <9 and thispos-9 not in visited and thispos-9 not in q:  # looking up and right
                    q.append(thispos-9)
                    
                if column > 0 and thispos-1 not in visited and thispos-1 not in q: # left
                    q.append(thispos-1)
                    
                if column < 9 and thispos+1 not in visited and thispos+1 not in q: # right
                    q.append(thispos+1)
                    
                if thispos < 90 and column > 0 and thispos+9 not in visited and thispos+9 not in q:  # down left
                    q.append(thispos+9)
                    
                if thispos < 90 and thispos+10 not in visited and thispos+10 not in q:    # down
                    q.append(thispos+10)
                    
                if thispos < 90 and column < 9 and thispos+11 not in visited and thispos+11 not in q:  # down right
                    q.append(thispos+11)
            

    def go(self):
        #after calling placeMines, this puts all the buttons back to their blank starting style
        for button in self.buttons:
            button.config(state="normal", text=" ", relief="raised", bg="lightgrey", image="")
        self.gameOn = True
        self.placeMines()


mine = App()
mine.geometry("800x800+200+200")
mine.title("Minesweeper")
mine.mainloop()
