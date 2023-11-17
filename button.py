import pygame

#button class
class Button():

	def __init__(self, x, y, surface, text="", width=120, height=50):
		text_colour = (0, 0, 0)
		font = pygame.font.SysFont("comicsans", 20)
		self.color = (255,255,255)
		self.rect = pygame.Rect(x,y,width,height)
		self.text = font.render(text,True, text_colour)
		self.text_x = x + 10
		self.text_y = y + 10
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		pygame.draw.rect(surface, self.color, self.rect)
		surface.blit(self.text,(self.text_x, self.text_y))

		return action
