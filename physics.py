from pygame import Vector2
from pygame import draw
from pygame.mouse import get_pressed, get_pos

from random import shuffle

class Cell:

    def __init__(self,pos,static=False):

        self.pos = Vector2(pos)
        self.prevpos = Vector2(pos)

        self.static = False
        self.ropes = []

        self.color = (150,150,150)
        self.radius = 5


    def update(self,DT):

        if not self.static:

            #gravity
            positionBeforeUpdate = self.pos

            self.pos += self.pos - self.prevpos
            self.pos += Vector2((0,200))*DT

            self.prevpos = positionBeforeUpdate
        
                

    def draw(self,window):

        draw.circle(window,self.color,self.pos,self.radius)


class Stick:


    def __init__(self,a,b,handler):

        self.a = a
        self.b = b

        self.handler = handler

        a.ropes.append(self)
        b.ropes.append(self)

        self.color = (150,150,150)
        self.length = a.pos.distance_to(b.pos)

    def destroy(self):

        self.a.ropes.remove(self)
        self.b.ropes.remove(self)
        self.handler.ropes.remove(self)

    def update(self,DT):

        distance = self.a.pos.distance_to(self.b.pos)
        offset = distance - self.length

        stickDir = (self.a.pos - self.b.pos).normalize()
        stickCenter = (self.a.pos + self.b.pos)/2


        if not self.a.static:
            self.a.pos = stickCenter + stickDir *  self.length/2

        if not self.b.static:
            self.b.pos = stickCenter - stickDir * self.length/2


        x,y = get_pos()
        l, _, _ = get_pressed()

        if stickCenter.distance_to((x,y)) <= 10:
            if l:
                self.destroy()

    def draw(self,window):

        draw.line(window,self.color,self.a.pos,self.b.pos,7)
        

class Cloth:

    def __init__(self,pos,size):

        self.pos = Vector2(pos)
        self.size = size   
        self.cells = []
        self.ropes = []

        self.spacing = 20
        self.buildCloth()

    def buildCloth(self):

        x,y = self.size


        for row in range(y):
            newrow = []

            for col in range(x):
                newrow.append(Cell(self.pos+Vector2(col*self.spacing,row*self.spacing)))


            self.cells.append(newrow)

        
        for row in range(y):

            for col in range(x):

                #right
                if col < x-1:
                    self.ropes.append(Stick(self.cells[row][col],self.cells[row][col+1],self))

                #down
                if row < y-1:
                    self.ropes.append(Stick(self.cells[row][col],self.cells[row+1][col],self))


        for col in range(x):

            if col % 3 == 0:
                self.cells[0][col].static = True


    def update(self,DT):
        
        shuffle(self.cells)

        for row in self.cells:
            for cell in row:
                cell.update(DT)


        for x in range(10):

            for rope in self.ropes:
                rope.update(DT)


    def draw(self,window):

        for row in self.cells:
            for cell in row:
                cell.draw(window)

        for rope in self.ropes:
            rope.draw(window)



