from tkinter import *
import random

class CheckersSquare(Canvas):
    '''Represents a Checkers square'''
    
    def __init__(self, master,r,c,bgColor):
        '''CheckersSquare(master,r,c,bgColor)
        Creates a new blank CheckersSquare at coordinate (r,c) with a given background color'''
        Canvas.__init__(self,master,width=50,height=50,bd=0)
        self.grid(row=r,column=c)
        self.coord = (r,c) # (row,column) coord
        self.index = r*8+c

        # set the background color and the highlight
        self.bgColor = bgColor
        self['highlightbackground'] = self.bgColor
        self['highlightthickness'] = 4
        self['bg'] = self.bgColor
        
        # set up listeners
        self.bind('<Button>',self.master.getClick)

    def getCoord(self):
        '''CheckersSquare.getCoord() -> tuple
        Returns the coordinate of the square'''
        return self.coord

    def highlightSquare(self):
        '''CheckersSquare.highlightSquare()
        highlights the square blue for a possible move'''
        self['highlightbackground'] = 'blue'

    def selectSquare(self):
        '''CheckersSquare.selectSquare()
        highlights the square black for a selected piece'''
        self['highlightbackground'] = 'black'

    def unHighlightSquare(self):
        '''CheckersSquare.unHighlightSquare()
        unhighlights the square by making the highlight the background color'''
        self['highlightbackground'] = self.bgColor

    def deletePiece(self):
        '''CheckersSquare.deletePiece()
        Deletes all widgets in the square (deletes nothing if empty square)'''
        widgetList = self.find_all() # remove existing widgets
        for widget in widgetList:
            self.delete(widget)
    
    def setColor(self,color):
        '''CheckersSquare.setColor(color)
        Deletes all pieces in the square and makes a new one with a given color'''
        self.deletePiece()
        self.create_oval(10,10,47,47,fill=color)

    def makeKing(self):
        '''CheckersSquare.makeKing()
        Adds a '*' on the piece to mark it as a king'''
        self.create_text(29,40,text='*',font=('Arial 40 bold'))

class CheckersBoard:
    '''Represents a board of Checkers'''

    def __init__(self):
        '''CheckersBoard()
        Creates a CheckersBoard in starting position
        0 = white, 0* = white king, 1 = red, 1* = red king, 2 = empty'''
        self.board = {} # dict to store position
        # create opening position
        for r in range(8):
            modNum = 1 - (r % 2)
            for c in range(8):
                coords = (r,c)
                if r < 3 and c % 2 == modNum:
                    self.board[coords] = '1 ' # player 1 (red)
                elif r > 4 and c % 2 == modNum:
                    self.board[coords] = '0 ' # player 0 (white)
                else:
                    self.board[coords] = '2 ' # empty
        self.currentPlayer = 1 # player 1 (red) starts
        self.gameOver = None # 0 = white wins, 1 = red wins

    def getPiece(self,coord):
        '''CheckersBoard.getPiece(coord) -> list
        Returns the piece at coord'''
        return [int(self.board[coord][0]),self.board[coord][1]]

    def getNumPieces(self):
        '''CheckersBoard.getNumPieces() -> tuple
        Returns the number of pieces for white and red'''
        boardList = list(self.board.values()) # list of board values
        pieces = [int(piece[0]) for piece in boardList] # list of pieces
        # the number of white pieces and the number of red pieces
        return pieces.count(0),pieces.count(1)

    def getGameOver(self):
        '''CheckersBoard.getGameOver() -> int
        Returns the gameOver attribute (0 = white, 1 = red, None = still playing)'''
        return self.gameOver

    def getPlayer(self):
        '''CheckersBoard.getPlayer() -> int
        Returns the current player'''
        return self.currentPlayer

    def nextPlayer(self):
        '''CheckersBoard.nextPlayer()
        Goes to the next player'''
        self.currentPlayer = 1 - self.currentPlayer

    def getPieceMoves(self,coord):
        '''CheckersBoard.getPieceMoves(coord) -> list
        Returns a list of the moves of the piece at coords
        Doesn't check if moves are legal (move to an open square)
        Jumping only checks if jumping over the opposite color'''
        r = coord[0]
        c = coord[1]
        moves = []
        # if not on the top and current player is white or red king, can move up
        if r != 0 and (self.currentPlayer == 0 or self.getPiece(coord)[1] == '*'):
            if c != 0: # if not on the left edge, can move left
                moves.append((r-1,c-1))
                # check for jumping
                if self.getPiece((r-1,c-1))[0] == 1-self.currentPlayer and \
                   r-1 != 0 and c-1 != 0:
                    moves.append((r-2,c-2))
            if c != 7: # if not on the right edge, can move right
                moves.append((r-1,c+1))
                # check for jumping
                if self.getPiece((r-1,c+1))[0] == 1-self.currentPlayer and \
                   r-1 != 0 and c+1 != 7:
                    moves.append((r-2,c+2))
        # if not on the bottom and current player is red or white king, can move down
        if r != 7 and (self.currentPlayer == 1 or self.getPiece(coord)[1] == '*'):
            if c != 0: # if not on the left edge, can move left
                moves.append((r+1,c-1))
                # check for jumping
                if self.getPiece((r+1,c-1))[0] == 1-self.currentPlayer and \
                   r+1 != 7 and c-1 != 0:
                    moves.append((r+2,c-2))
            if c != 7: # if not on the right edge, can move right
                moves.append((r+1,c+1))
                # check for jumping (not on edge, jumping over opposite colored piece
                if self.getPiece((r+1,c+1))[0] == 1-self.currentPlayer and \
                   r+1 != 7 and c+1 != 7:
                    moves.append((r+2,c+2))
        return moves # return the list of moves

    def getLegalMoves(self,coord):
        '''CheckersBoard.getLegalMoves() -> list
        Returns a list of the current player's legal moves with the piece at coord'''
        legalMoves = [] # all legal moves
        allMoves = self.getPieceMoves(coord) # all moves
        canJump = False # if there is a jump, the player must jump

        # check if the piece can jump
        for move in allMoves:
            # abs(move[0]-coord[0]) == 2 --> the column always changes by +-2 if jumping
            if abs(move[0]-coord[0]) == 2 and self.getPiece(move)[0] == 2: # jumping and empty square
                canJump = True

        # get all legal moves
        for move in allMoves:
            # if there is a jump and the move is a jump and to an empty square, it is legal
            # otherwise if there isn't a jump and the move is to an empty square, it is legal
            if (canJump and abs(move[0]-coord[0]) == 2) or not canJump:
                if self.getPiece(move)[0] == 2:
                    legalMoves.append(move)

        return legalMoves # return the list of legal moves

    def tryMove(self,startCoord,endCoord):
        '''CheckersBoard.tryMove()
        Tries to move a piece from startCoord to endCoord, does nothing if move is not legal
        If the piece is on the last row for its color, it becomes a king'''
        moves = self.getLegalMoves(startCoord) # get all legal moves for the piece on startCoord
        endTurn = True # the turn is done or still going (jumping)
        moved = False # the move is legal or not
        if endCoord in moves: # the move is legal
            moved = True
            # difference is to see if the move was a jump or not (2 = jump, 1 = move)
            difference = [endCoord[0]-startCoord[0], endCoord[1]-startCoord[1]]

            # check if the piece is a king
            king = ' '
            if endCoord[0] == self.currentPlayer == 0 or \
               (endCoord[0] == 7 and self.currentPlayer == 1) or \
               self.board[startCoord][1] == '*':
                king = '*'

            # move the piece
            self.board[startCoord] = '2 '
            self.board[endCoord] = str(self.currentPlayer) + king

            if abs(difference[0]) == 2: # jumped piece
                # difference[0]/2 and difference[1]/2 = 1 or -1 and is the piece between the start and end squares
                jumpedPiece = (startCoord[0]+difference[0]/2, startCoord[1]+difference[1]/2)
                self.board[jumpedPiece] = '2 ' # take the jumped piece

                # check if piece can still jump
                newMoves = self.getLegalMoves(endCoord)
                for move in newMoves: # all new legal moves
                    if abs(move[0]-endCoord[0]) == 2: # can jump
                        endTurn = False

            # if the turn has ended (not still jumping), go to next player and check for game over
            if endTurn:
                self.nextPlayer()
                self.gameOver = self.checkGameOver()

        return moved,endTurn # returnd moved and endTurn

    def checkGameOver(self):
        '''CheckersBoard.checkGameOver() -> int
        Checks if the game is over
        Returns 0 if white won, 1 if red won, and None if the game is still going'''
        # get all the player pieces by their coordinates
        playerPieces = []
        for key in self.board.keys(): # get all the keys of the board
            if self.getPiece(key)[0] == self.currentPlayer: # if the piece is the current player's color
                playerPieces.append(key)

        # check if the player can move
        gameOver = True
        for piece in playerPieces: # go through each piece
            if len(self.getLegalMoves(piece)) > 0: # if the piece has a legal move, game is not over
                gameOver = False
        if gameOver: # game over, return who won
            if self.currentPlayer == 0:
                return 1
            else:
                return 0

class CheckersFrame(Frame):
    '''Frame to play Checkers'''

    def __init__(self,master,name1,name2):
        '''CheckersFrame(master,name1,name2)
        Creates a new blank CheckersFrame with the player's name'''
        # set up Frame object
        Frame.__init__(self,master,bg='white')
        self.grid()

        # set up game data
        self.players = (name1, name2)
        self.colors = ('white','red')
        self.piece = (0,0)
        self.jumping = False

        # create player labels
        Label(self,text=self.players[0],font=('Arial',16),bg='white').grid(row=0,column=1,columnspan=3,sticky=W,padx=10)
        self.p1Sq = CheckersSquare(self,0,0,'light grey')
        self.p1Sq.unbind('<Button>')
        self.p1Sq.setColor(self.colors[0])
        Label(self,text=self.players[1],font=('Arial',16),bg='white').grid(row=0,column=4,columnspan=3,sticky=E,padx=10)
        self.p2Sq = CheckersSquare(self,0,7,'light grey')
        self.p2Sq.setColor(self.colors[1])
        self.p2Sq.unbind('<Button>')
        self.rowconfigure(1,minsize=3)

        # create board and squares
        self.board = CheckersBoard()
        self.squares = {}
        for r in range(8):
            for c in range(8):
                rc = (r,c)
                if r % 2 == c % 2 == 0:
                    bgColor = 'blanched almond'
                elif c % 2 == r % 2 == 1:
                    bgColor = 'blanched almond'
                else:
                    bgColor = 'dark green'
                self.squares[rc] = CheckersSquare(self,r+2,c,bgColor)

        # set up turn markers
        self.rowconfigure(11,minsize=3)
        self.turnLabel = Label(self,text='Turn:',font=('Arial',16),bg='white')
        self.turnLabel.grid(row=12,column=3)
        self.turnSq = CheckersSquare(self,12,4,'light grey')
        self.turnSq.setColor(self.colors[1])
        self.turnSq.unbind('<Button>')

        self.updateDisplay()

    def highlightMoves(self):
        '''CheckersFrame.highlightMoves()
        Highlights the legal moves of the selected piece'''
        moves = self.board.getLegalMoves(self.piece) # get all legal moves
        for move in moves: # highlight legal moves
            self.squares[move].highlightSquare()

    def unHighlightAll(self):
        '''CheckersFrame.unHighlightAll()
        Unhighlights all squares (sets each highlight to background color)'''
        for r in range(8):
            for c in range(8):
                self.squares[(r,c)].unHighlightSquare()

    def resetGame(self):
        '''CheckersFrame.resetGame()
        Resets the board to play another game of checkers'''
        # destroy win label and reset button
        self.resetBtn.destroy()
        self.gameOverLabel.destroy()
        # make turn indicator
        self.turnLabel = Label(self,text='Turn:',font=('Arial',16),bg='white')
        self.turnLabel.grid(row=12,column=3)
        self.turnSq = CheckersSquare(self,12,4,'light grey')
        self.turnSq.setColor(self.colors[1])
        self.turnSq.unbind('<Button>')
        # reset board
        self.board = CheckersBoard()
        self.unHighlightAll()
        self.updateDisplay()

    def updateDisplay(self):
        '''CheckersFrame.updateDisplay()
        Updates each square with the right piece and changes the turn indicator
        Checks if the game is over'''
        # update squares
        for r in range(8):
            for c in range(8):
                rc = (r,c)
                piece = self.board.getPiece(rc)
                if piece[0] == 2: # empty square
                    self.squares[rc].deletePiece()
                else: # square with piece
                    self.squares[rc].setColor(self.colors[piece[0]])
                    if piece[1] == '*': # king
                        self.squares[rc].makeKing()

        # update turn indicator
        self.turnSq.setColor(self.colors[self.board.getPlayer()])

        # check for game over
        gameOver = self.board.getGameOver()
        if gameOver != None: # game over
            # delete the turn indicators
            self.turnSq.destroy()
            self.turnLabel.destroy()
            # make reset button
            self.resetBtn = Button(self,text='Reset',command=self.resetGame)
            self.resetBtn.grid(row=0,column=3,columnspan=2)
            # say who wins
            winner = self.players[gameOver]
            gameOverMessage = '{} wins!'.format(winner.title())
            self.gameOverLabel = Label(self,text=gameOverMessage,font=('Arial',18),bg='white')
            self.gameOverLabel.grid(row=10,column=2,columnspan=4)

    def getClick(self,event):
        '''CheckersFrame.getClick(event)
        When the user clicks get the square clicked a move a piece or choose a piece to move'''
        windowCoord = event.widget.getCoord() # get the coordinate
        coord = (windowCoord[0]-2,windowCoord[1]) # remove 2 extra rows on top
        # unhighlight all squares if not currently jumping
        if not self.jumping:
            self.unHighlightAll()

        # the first click (clicked a piece and not jumping)
        if self.board.getPiece(coord)[0] == self.board.getPlayer() and not self.jumping:
            self.squares[coord].selectSquare()
            self.piece = coord # save the piece that is moving
            self.highlightMoves()
        else: # attempt to move the piece selected
            moved,endTurn = self.board.tryMove(self.piece,coord)
            if moved: # piece moved, not jumping and unhighlight all
                self.jumping = False
                self.unHighlightAll()
                self.squares[coord].selectSquare()
            if not endTurn: # still jumping, highlight legal moves
                self.jumping = True
                self.piece = coord
                self.highlightMoves()
        self.updateDisplay() # update display

def Checkers():
    '''Checkers()
    plays Checkers'''
    name1 = input("Enter the name for red: ")
    name2 = input("Enter the name for white: ")
    root = Tk()
    root.title('Checkers')
    game = CheckersFrame(root,name2,name1)
    game.mainloop()

Checkers()
