from scene import *
import random, sound
from arrows import *

sw, sh = get_screen_size()
rect_w = sw/3  #343.33
rect_h = 612 #668
side = int(rect_w/10) 
colors = ['red', 'orange', 'yellow']
grounded_blocks = []

new = False
A = Action


class Board(ShapeNode, SpriteNode):
	def __init__(self, stroke_color='lightgrey', line_width=1, parent=None, *args, **kwargs):
			path = ui.Path.rect(0, 0, rect_w, rect_h)
			path.line_width = line_width
			
			if stroke_color == 'lightgrey':
				d = int(rect_w/10)
				for l in range(int(rect_w/d)):
					x = l*d
					path.move_to(x, 0)
					path.line_to(x, rect_h)
			
			super().__init__(path,
							 fill_color='white',
							 stroke_color=stroke_color,
							 parent=parent,
							 *args, **kwargs)
		

class Shape(SpriteNode):
	def __init__(self):
		
		self.RIGHT = False
		self.LEFT = False
		
		self.num = random.randrange(0, 3)
		
		x = random.randrange(int(-rect_w/2), int(rect_w/2) - self.num*side, side) + side/2
		y = rect_h/2 - side/2
		
		dot =  [[
				  [x, y]
						 ]]
		 		
		line = [
				 [[x, y], [x+side, y]],
				 [[x, y], [x, y-side]]
									   ]
									   
		Z = [
			  [[x, y], [x+side, y], [x+side, y-side], [x + 2*side, y-side]],
			  [[x+side, y], [x+side, y-side], [x, y-side], [x, y - 2*side]]
			  																]
			  
			  
		
		self.shapes = [dot, line, Z]
		
		#num chooses from list of shapes
		self.shape = self.shapes[self.num]
		#var chooses the rotation of the shape
		self.var = random.choice(range(len(self.shape)))
		
		self.figure = []
		
		for pos in self.shape[self.var]:
			block = SpriteNode('pzl:Yellow3', 
								position=(pos[0], pos[1]), 
								color=colors[self.shapes.index(self.shape)],
								size=(side, side))
			self.figure.append(block)
			
					
	def move_down(self):
		for block in self.figure:
			y = block.position.y - side
			block.position = Point(block.position.x, y) 
		
				
	def left_right(self):
		if self.RIGHT:
			#chooses the rightest block
			right_x = max([b.position.x for b in self.figure])
			#checks that the block isn't getting out of frame
			if right_x != 153:
				for block in self.figure:
					x = block.position.x + side
					block.position = Point(x, block.position.y)
			self.RIGHT = False
						
		elif self.LEFT:
			left_x = min([b.position.x for b in self.figure])
			if left_x != -153:
				for block in self.figure:
					x = block.position.x - side
					block.position = Point(x, block.position.y)
		self.LEFT = False
		
	
	def rotate_shape(self):
		#to know in which rotation the figure was before rotation
		self.var += 1
		if self.var >= len(self.shape):
			self.var = 0
			
		#other blocks will move around the root_block
		root_block = self.figure[len(self.figure)//2]
		x, y = root_block.position
		#p1 - blocks that were to the left (or upper) of root_block, p2 - to the right (or lower)
		p1 = [self.figure[i] for i in range(self.figure.index(root_block))]
		p2 = [self.figure[i] for i in range(self.figure.index(root_block)+1, len(self.figure))]
		
		for block in p1:
			if self.var == 0:
				x = block.position.x - side
				y = block.position.y - side
				block.position = Point(x, y)
			elif self.var == 1:
				x = block.position.x + side
				y = block.position.y + side
				block.position = Point(x, y)
			
	
	def if_grounded(self):
		for block in self.figure:
			if block.position.y < -rect_h/2 + side:
				return True
			else:
				for b in grounded_blocks:
					if (block.position.x == b.position.x) and (block.position.y - side == b.position.y):
						return True


class Game(Scene):
	def setup(self):
		self.background_color = 'white'
		self.grey_rect = Board(line_width=2, parent=self, position=(sw/3, sh/2), z_position=0)
		self.board = Board(stroke_color='purple', line_width=15, parent=self, position=(sw/3, sh/2), 		z_position=-1)
		
		self.seconds = 0
		self.figure = None
		self.add_buttons()
		self.add_figure()
	
	
	def update(self):
		self.seconds += self.dt
		if self.seconds > 0.3:
			self.seconds = 0
			if not self.figure.if_grounded():
				self.figure.move_down()
			else:
				for block in self.figure.figure:
					grounded_blocks.append(block)
					self.figure.figure = []
				global new
				new = True
				
			if new:
				self.add_figure()
		
			
	def touch_began(self, touch):
		tapped = True
		for arw in self.arrows:
			if touch.location in arw.frame:
				sound.play_effect('rpg:Chop')
				arw.fill_color = '#969696'
				
				if 'right' in arw.icon:
					self.figure.RIGHT = True
					self.figure.left_right()
					
				elif 'left' in arw.icon:
					self.figure.LEFT = True
					self.figure.left_right()
					
				elif 'up' in arw.icon:
					self.figure.rotate_shape()
			
	
	def touch_ended(self, touch):
		for arw in self.arrows:
			if arw.fill_color == '#969696':
				arw.fill_color = 'white'
				

	def add_buttons(self):
		self.arrows = [Arrow(i, position=icons[i], parent=self) for i in icons] 
		

	def add_figure(self):
		self.figure = Shape()
		for block in self.figure.figure:
			self.grey_rect.add_child(block)
			global new
			new = False
			
			

run(Game()) 
