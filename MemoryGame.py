import random
import os
import java.awt.Font as Font
import java.awt.FontMetrics
#http://www.java2s.com/Tutorial/Java/0261__2D-Graphics/Centertext.htm
#Drawing centered text, should figure this out someday
class Coords:
  def __init__(self,i):
    self.x = i%cols
    self.y = i//cols
    
def intToCoord(i):#Converts an integer to coordinates, given the column count of the coordinates
  return Coords(i) #returns in y, x format
  
def coordToInt(coord):
  return coord.x+coord.y*cols
  
def hideCardAtCoord(coord):
  offsetX = margins + coord.x*(margins+cardWidth)
  offsetY = margins + coord.y*(margins+cardHeight)
  addRectFilled(boardImage, offsetX, offsetY, cardWidth, cardHeight, cardBackColor)
  i = coordToInt(coord)
  addTextWithStyle(boardImage,offsetX+cardWidth/2 - 10,offsetY+cardHeight/2 + 10,"%d"%i,makeStyle("Times New Roman",Font.BOLD,48))
  
def hideCardAtXY(x,y):
  hideCardAtCoord(Coord(x,y))
  
def randomizeBoard():
  for y in range(0,rows):
    for x in range(0,cols):
      rx = random.randint(0,cols-1)
      ry = random.randint(0,rows-1)
      tempint = board[y][x]
      board[y][x] = board[ry][rx]
      board[ry][rx] = tempint
      
def hideAllCards():
  for y in range(0,rows):
    for x in range(0,cols):
      hideCardAtCoord(Coords(x+y*cols))
      
def clearCardAtCoord(coord):
  offsetX = margins + coord.x*(margins+cardWidth)
  offsetY = margins + coord.y*(margins+cardHeight)
  addRectFilled(boardImage, offsetX, offsetY, cardWidth, cardHeight, backgroundColor)
  
def clearCardAtXY(x,y):
  clearCardAtCoord(Coord(x,y))
  
def showCardAtCoord(coord):
  offsetX = margins + coord.x*(margins+cardWidth)
  offsetY = margins + coord.y*(margins+cardHeight)
  copyInto(images[board[coord.y][coord.x]],boardImage,offsetX,offsetY)
  
def showCardAtXY(x,y):
  showCardAtCoord(Coord(x,y))
  
def scalePercent(pic,percent):
  percent = percent*0.01
  w1 = getWidth(pic)
  h1 = getHeight(pic)
  w2 = int(getWidth(pic)*percent)
  h2 = int(getHeight(pic)*percent)
  newpic = makeEmptyPicture(w2, h2)
  for y in range(0,h2):
    for x in range(0,w2):
      drawn = getPixel(newpic,x,y)
      sampled = getPixel(pic,int(x/percent),int(y/percent))
      setColor(drawn,getColor(sampled))
  return newpic

def getInput():
  Prompt = "Type a number from 0-11"
  while true:
    i = requestString(Prompt)
    if i.isnumeric():
      i = int(i)
      if i >= 0 and i <= 11:
        c = intToCoord(i)
        if board[c.y][c.x] == -1:
          Prompt = "You've already matched that card"
        else:
          if i == guessOne:
            Prompt = "That card is already being shown."
          else:
            break
      else:
        Prompt = "That isn't a valid number (between 0 and 11)"
    else:
      Prompt = "That isn't a number."
  return i

boardWidth = 800
boardHeight = 600
cols = 4
rows = 3
margins = 5
cardWidth = (boardWidth-margins*(cols+1))/cols
cardHeight = (boardHeight-margins*(rows+1))/rows
cardBackColor = makeColor(127,127,127)
backgroundColor = makeColor(31,31,31)
boardImage = makeEmptyPicture(800,600)
board =  [[0,0,1,1],
          [2,2,3,3],
          [4,4,5,5]]
imageFolder = os.path.dirname(os.path.abspath(__file__))+r"\MemoryGameImages"
images = []
maxint = 5
validIndexes = []
print("Resizing images in folder.")
for i in range(0,6):
  validIndexes.append(i)
for i in range(0,6):
  ri = random.randint(0,maxint)
  resized = makePicture(imageFolder+"\\%02d.png"%validIndexes[ri])
  validIndexes[ri] = validIndexes[maxint]
  ratio = cardWidth/float(getWidth(resized)) #Percent required to match width
  if ratio > cardHeight/float(getHeight(resized)):
    ratio = cardHeight/float(getHeight(resized)) #Percent required to match height
  #Rescale by the smaller ratio, to ensure the new image fits into the card area, even if it isn't square
  resized = scalePercent(resized,ratio*100)
  images.append(resized)
  maxint -= 1
randomizeBoard()
hideAllCards()
show(boardImage)
print board
wrongTurns = 0
matchesMade = 0
while true:
  guessOne = -1 #Reset guessOne, this variable is used in the getInput function, so you can't pick the same card twice.
  i1 = getInput()
  c1 = intToCoord(i1)
  showCardAtCoord(c1)
  repaint(boardImage)
  guessOne = i1

  i2 = getInput()
  c2 = intToCoord(i2)
  showCardAtCoord(c2)
  repaint(boardImage)

  if board[c1.y][c1.x] == board[c2.y][c2.x]:
    board[c1.y][c1.x] = -1
    board[c2.y][c2.x] = -1
    showInformation("Match!")
    clearCardAtCoord(c1)
    clearCardAtCoord(c2)
    matchesMade +=1
    if matchesMade >=6:
      showInformation("You win!")
      break
  else:

    wrongTurns += 1
    showInformation("No match! %d/6 wrong moves"%wrongTurns)
    hideCardAtCoord(c1)
    hideCardAtCoord(c2)
    if wrongTurns >= 6:
      showInformation("You lose!")
      break
  repaint(boardImage)
