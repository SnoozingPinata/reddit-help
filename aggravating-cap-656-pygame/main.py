import pygame
from pygame.color import THECOLORS


class GameObject:
  def __init__(self, size, speed, direction, x, y, color):
    self.size = size
    self.speed = speed
    self.direction = direction
    self.x = x
    self.y = y
    self.color = color
  
  def update(self):
    pass

  def draw(self, surface):
    pygame.draw.rect(surface, self.color, [self.x, self.y, self.size, self.size])


class Game:
	def __init__(self):
		self.windowSize = (360, 480)
		self.title = 'Plane Game'
		pygame.init()
		self.window = pygame.display.set_mode(self.windowSize)
		self.surface = pygame.Surface(self.windowSize)
		pygame.display.set_caption(self.title)
		self.object_list = []
		self.player = None

	def onStart(self):
		# Clearing out the object list and the player target so this function gets the game back to a clean slate
		self.player = None
		self.object_list.clear()
		player = GameObject( size=50, speed=2, direction=1, x=0, y=0, color=THECOLORS['yellow'] )
		self.player = player
		enemy1 = GameObject( size=20, speed=4, direction=-1, x=150, y=150, color=THECOLORS['red'] )
		self.object_list.append(enemy1)

	def run(self):
		self.onStart()
		self.running = True
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
			self.update()
			self.draw()
		pygame.quit()

	def draw(self):
		# clear frame
		self.surface.fill(THECOLORS['white'])

		# draw objects
		for object in self.object_list:
			object.draw(self.surface)

		# draw player
		self.player.draw(self.surface)

		# update window
		self.window.blit(self.surface, (0, 0))
		pygame.display.flip()

	def update(self):
		# update the player first :P
		self.handle_input()
		self.player.update()
		# update everything in the object list next
		for object in self.object_list:
			object.update()
	
	def handle_input(self):
		# edit this function to look at the pygame keys and move the self.player object by manipulating its x and y values
		pass


if __name__ == '__main__':
	Game().run()