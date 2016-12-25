#!/usr/bin/env python
import pygame
from pygame import font
import math
pygame.init();

print pygame.font.get_default_font()

#Define colors
black	= (0,0,0)
white	= (255,255,255)
green	= (0,255,0)
red	= (255,0,0)
grey	= (128,128,128)

size=(1024,768)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Test Screen")
background = pygame.Surface(screen.get_size())
done=False

class Guy(pygame.sprite.Sprite):
	def __init__(self,vector,startx,starty):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('gfx/guy.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.topleft = [startx,starty]
		self.vector = vector
		self.startx = startx
		self.starty = starty
        def update(self):
                newpos = self.calcnewpos(self.rect,self.vector)
                self.rect = newpos
                background.blit(self.image, self.rect)
        def calcnewpos(self,rect,vector):
                (angle,z) = vector
                (dx, dy) = (z*math.cos(angle),z*math.sin(angle))
                return rect.move(dx,dy)
	def reset(self):
		self.rect.topleft = [self.startx,self.starty]
		background.blit(self.image,self.rect)
class Vehicle(pygame.sprite.Sprite):
        def update(self):
                newpos = self.calcnewpos(self.rect,self.vector)
                self.rect = newpos
                self.CheckOutOfScreen()
                background.blit(self.image, self.rect)
        def calcnewpos(self,rect,vector):
                (angle,z) = vector
                (dx, dy) = (z*math.cos(angle),z*math.sin(angle))
                return rect.move(dx,dy)
        def CheckOutOfScreen(self):
                if self.startpos[0] == left and self.rect.left > right:
                        self.reset()
                elif self.startpos[0] == right and self.rect.right < left:
                        self.reset()
        def reset(self):
                if self.vector[0] > 0.5*math.pi or self.vector[0] > 1.5*math.pi:
                        self.rect.topleft = self.startpos
                elif self.vector[0] < 0.5*math.pi or self.vector[0] < 1.5*math.pi:
                        self.rect.topright = self.startpos
                background.blit(self.image,self.rect)

class TukTuk(Vehicle):
	def __init__(self,vector,startpos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('gfx/tuktuk_l.png').convert_alpha()
		print vector
		if vector[0] > 0.5*math.pi or vector[0] > 1.5*math.pi:
			self.image = pygame.image.load('gfx/tuktuk_r.png').convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.topright = startpos
		elif vector[0] < 0.5*math.pi or vector[0] < 1.5*math.pi:
			self.rect = self.image.get_rect()
			self.rect.topleft = startpos
		self.area = screen.get_rect()
		self.vector = vector
		self.startpos = startpos

class Tata(Vehicle):
        def __init__(self,vector,startpos):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load('gfx/tata_l.png').convert_alpha()
                print vector
                if vector[0] > 0.5*math.pi or vector[0] > 1.5*math.pi:
                        self.image = pygame.image.load('gfx/tata_l.png').convert_alpha()
                        self.rect = self.image.get_rect()
                        self.rect.topright = startpos
                elif vector[0] < 0.5*math.pi or vector[0] < 1.5*math.pi:
                        self.rect = self.image.get_rect()
                        self.rect.topleft = startpos
                self.area = screen.get_rect()
                self.vector = vector
                self.startpos = startpos

class Goal(pygame.sprite.Sprite):
	def __init__(self,position,width,heigth):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width,heigth])
		self.image.fill(red)
		self.rect = self.image.get_rect()
		self.position=position
	def update(self):
		background.blit(self.image,self.rect)
		self.rect.topleft = self.position

class GameTimer(pygame.sprite.Sprite):
	def __init__(self,position,width,heigth):
		pygame.sprite.Sprite.__init__(self)
		self.font=pygame.font.SysFont("freesans", 72)
		self.position=position
		self.width=width
		self.heigth = heigth
	def update(self):
		playingtime = str(pygame.time.get_ticks() / 1000)
		self.image = self.font.render(playingtime, 0 , red)
		self.rect = self.image.get_rect()
		self.rect.topleft = self.position
		background.blit(self.image,self.rect)
def drawlandscape():
	background.fill(white)
	pygame.draw.rect(background,grey,[0,100,1024,300])
        pygame.draw.rect(background,grey,[0,425,1024,300])

def steuerung(event):
	vector=[0,0]
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                        vector=[0.5*math.pi,5]
                elif event.key == pygame.K_UP:
                        vector=[1.5*math.pi,5]
                elif event.key == pygame.K_RIGHT:
                        vector=[0,5]
                elif event.key == pygame.K_LEFT:
                        vector=[math.pi,5]
        if event.type == pygame.KEYUP:
                vector=[0,0]
	return vector

clock=pygame.time.Clock()
player=Guy([0,0],size[0]//2-50,0)
lanes=[100,200,300,425,525,625]
left=0
right=size[0]
tata=Tata([0,10],[left,lanes[4]])
tuktuk=TukTuk([0,10],[left,lanes[0]])
tuktuk2=TukTuk([0,5],[left,lanes[1]])
tuktuk3=TukTuk([0,15],[left,lanes[2]])
tuktuk4=TukTuk([math.pi,10],[right,lanes[3]])
vehicles=[tata,tuktuk,tuktuk2,tuktuk3,tuktuk4]
gametime = GameTimer([0,0],100,100)
goal = Goal([size[0]/2-50,size[1]-50],100,50)
#Main Loop
while done==False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done=True
		elif event.type == pygame.KEYDOWN and  event.key == pygame.K_ESCAPE:
                        done = True

	drawlandscape()
	player.vector=steuerung(event) #event
	# Update Vehicles
	for v in vehicles:
		v.update()
		is_a_collision = pygame.sprite.collide_mask(v,player)
		if is_a_collision != None:
			player.reset()
	player.update()
	goal.update()
	gametime.update()
	clock.tick(30)
	screen.blit(background, (0,0))
	pygame.display.flip()
pygame.quit()
