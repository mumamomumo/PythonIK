import math
import pygame
from pygame.locals import *
from typing import overload


pygame.init()

WIN_HEIGHT = 800
WIN_WIDTH = 1000
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


clock = pygame.time.Clock()



class Vector:
    def __init__(self, endX: float, endY: float, offsetX:float = 0, offsetY:float = 0):
        self.x = endX+offsetX
        self.y = endY+offsetY
        self.position = [self.x, self.y]
        self.localPosition = [endX, endY]
        self.offset = [offsetX, offsetY]
        self.magnitude = math.sqrt(self.localPosition[0]**2 + self.localPosition[1]**2)
    
    def update_pos(self, newX: float, newY: float):
        self.x = newX
        self.y = newY
        self.position = [self.x, self.y]
        self.localPosition = [newX-self.offset[0], newY-self.offset[1]]
        
        self.magnitude = math.sqrt(self.localPosition[0]**2 + self.localPosition[1]**2)

    def update_offset(self, offsetX: float, offsetY:float):
        
        self.offset = [offsetX, offsetY]
        self.localPosition = [self.position[0]-self.offset[0], self.position[1]-self.offset[1]]
        self.magnitude = math.sqrt(self.localPosition[0]**2 + self.localPosition[1]**2)

    





class Vector2(Vector):
    
    def __add__(self, point: Vector):
        newX = self.x + point.x-self.offset[0]
        newY = self.y + point.y-self.offset[1]
        return Vector2(newX, newY, self.offset[0], self.offset[1])

    def __sub__(self, point:Vector): 
        newX = self.localPosition[0] - point.localPosition[0]
        newY = self.localPosition[1] - point.localPosition[1]
        newV = Vector2(newX, newY, self.offset[0], self.offset[1])
        newV.update_offset(point.x, point.y)
        return newV
    
    def __mul__(self, value:float):
        newX = self.localPosition[0]*value
        newY = self.localPosition[1]*value
        return Vector2(newX, newY, self.offset[0], self.offset[1])
    
    def __truediv__(self, value:float):
        newX = self.x/value
        newY = self.x/value
        return Vector2(newX, newY, self.offset[0], self.offset[1])
    
    def Distance(point1: Vector, point2:Vector):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def Dot(self, point: Vector):
        return self.localPosition[0]*point.localPosition[0]+self.localPosition[1]*point.localPosition[1]
    
    def Angle(point1: Vector, point2: Vector):
        step1 = point1.Dot(point2)
        step2 = round(step1/(point1.magnitude*point2.magnitude), 8)
        angle = round(math.acos(step2)*180/math.pi, 4)
        return angle
    
    def SignedAngle(point1: Vector, point2: Vector):
        x1, y1 = point1.localPosition
        x2, y2 = point2.localPosition
        a = round(math.atan2(x1*y2-y1*x2,x1*x2+y1*y2)*(180/math.pi), 4)
        return -a
    
    def Rotate(vector: Vector, theta: float, deg:bool = False):
        x = vector.localPosition[0]
        y = vector.localPosition[1]
        if deg: theta*=-math.pi/180
        return Vector2(round(x*math.cos(theta)-y*math.sin(theta), 4), round(x*math.sin(theta)+y*math.cos(theta), 4), *vector.offset)
    
    def ClampAngle(self, vector2: Vector, minAngle: float, maxAngle: float):
        angle = Vector2.SignedAngle(self, vector2)
        diff=0
        if angle<minAngle:
            diff = round(minAngle-angle, 4)
        elif angle>maxAngle:
            diff = round(maxAngle-angle, 4)
        if (diff != 0):
            newV = Vector2.Rotate(self, diff, True)
            self.update_pos(*newV.position)
        
    def SetAngle(self, vector1: Vector, angle: float):
        newV = Vector2.Rotate(vector1, angle, True)
        
        
        return Vector2(*newV.localPosition, *self.offset)
    
    def normalize(self):
        newX = round(self.localPosition[0]/self.magnitude, 8)
        newY = round(self.localPosition[1]/self.magnitude, 8)
        self.position = [newX+self.offset[0], newY+self.offset[1]]
        self.localPosition = [newX, newY]
        return Vector2(newX, newY, self.offset[0], self.offset[1])




offsetX = WIN_WIDTH//2-400
offsetY = WIN_HEIGHT//2-200
point1 = Vector2(430, 430, offsetX, offsetY)
point1Length = 250
point2 = Vector2(430, 430, *point1.position)
point2Length = 250

point3 = Vector2(600, 600)


point1Circle = pygame.draw.circle(WIN, "yellow", point1.position, 7)
point2Circle = pygame.draw.circle(WIN, "orange", point2.position, 7)
point3Circle = pygame.draw.circle(WIN, "red", point3.position, 7)


movePoint3 = False
movePoint2 = False
movePoint1 = False
font = pygame.font.Font('freesansbold.ttf', 32)



run = True
while run:
    WIN.fill(0)
    # clock.tick(60)
    mouseX, mouseY = pygame.mouse.get_pos()
    keypressed = pygame.key.get_pressed()


    if (movePoint3): point3.update_pos(mouseX, mouseY)
    point2.update_pos(*point3.position)
    
    
    

    
    newV = point2-point3
    newV = Vector2(round(newV.localPosition[0], 4), round(newV.localPosition[1], 4))
    point1 += Vector2(0, 0)-newV
    point2 = point2.SetAngle(point1, abs(Vector2.SignedAngle(point1, point2)))
    point1 = point1.normalize()*point1Length
    point2 = point2.normalize()*point2Length
    
    point2.update_offset(*point1.position)
    point3.update_offset(*point2.position)
    
    if (pygame.mouse.get_pressed()[0] and point3Circle.collidepoint(mouseX, mouseY)): movePoint3 = True

    
    text = font.render(f"{Vector2.SignedAngle(point1, point2)} degrees", True, "green")
    textRect = text.get_rect()
    textRect.topleft = [50, 50]
    


    if (pygame.mouse.get_pressed()[2] and movePoint1): movePoint1 = False
    if (pygame.mouse.get_pressed()[2] and movePoint2): movePoint2 = False
    if (pygame.mouse.get_pressed()[2] and movePoint3): movePoint3 = False
    
    
    pygame.draw.line(WIN, "yellow", point1.position, point1.offset, 4)
    pygame.draw.line(WIN, "orange", point2.position, point2.offset, 4)
    pygame.draw.line(WIN, "red", point3.position, point3.offset, 4)
    pygame.draw.line(WIN, "Red", [offsetX, offsetY], [offsetX, WIN_HEIGHT], 4)
    pygame.draw.line(WIN, "Red", [offsetX, offsetY], [WIN_WIDTH, offsetY], 4)
    WIN.blit(text, textRect)

    

    point1Circle = pygame.draw.circle(WIN, "yellow", point1.position, 7)
    point2Circle = pygame.draw.circle(WIN, "orange", point2.position, 7)
    point3Circle = pygame.draw.circle(WIN, "red", point3.position, 7)
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            break
