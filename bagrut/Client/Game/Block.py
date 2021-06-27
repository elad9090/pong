import pygame


class Block(pygame.sprite.Sprite):
	def __init__(self, path, x_pos, y_pos):
		super().__init__()
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect(center=(x_pos, y_pos))

	@property
	def x(self):
		return self.rect.centerx

	@x.setter
	def x(self, v):
		self.rect.centerx = v
	
	@property
	def y(self):
		return self.rect.centery

	@y.setter
	def y(self, v):
		self.rect.centery = v
