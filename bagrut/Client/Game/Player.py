from .Block import Block
from . import screen_height


class Player(Block):
	def __init__(self, path, x_pos, y_pos, speed, is_comp=False):
		super().__init__(path, x_pos, y_pos)
		self.score = 0
		self.speed = speed
		self.movement = 0
		self.ready = False
		self.__comp = is_comp

	def screen_constrain(self):
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= screen_height:
			self.rect.bottom = screen_height

	def update(self, ball_group = None):
		if not self.__comp:
			self.rect.y += self.movement
		else:
			if self.rect.top < ball_group.sprite.rect.y:
				self.rect.y += self.speed
			if self.rect.bottom > ball_group.sprite.rect.y:
				self.rect.y -= self.speed
		self.screen_constrain()

	def is_comp(self, val = None):
		if val is None:
			return self.__comp
		self.__comp = val
		return val

	def pickle(self):
		return f'{self.y},{self.ready}'
