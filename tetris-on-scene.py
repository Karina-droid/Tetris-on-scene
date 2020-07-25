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
			
			self.figure = None
			
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
		
		x = random.randrange(int(-rect_w/2) + side, int(rect_w/2) - self.num*side, side) + side/2
		y = rect_h/2 - side/2
		
		dot =  [[
				  [0, 0]
						 ]]
		 		
		line = [
				 [[0, 0], [-side, 0]],
				 [[0, 0], [0, -side]]
									  ]
									   
		Z = [
			  [[0, 0], [-side, 0], [0, -side], [side, -side]],
			  [[0, 0], [0, -side], [-side, -side], [-side, -2*side]]
			  												   		 ]
			  
			  
		
		self.shapes = [dot, line, Z]
		
		#num chooses from list of shapes
		self.shape = self.shapes[self.num]
		#var chooses the rotation of the shape
		self.var = random.choice(range(len(self.shape)))
		
		#rows show how many blocks in each row. if in any is 10 - delete_row()
		self.rows = [0 for i in range(18)]
		self.delete = None
		
		self.figure = []
		
		for pos in self.shape[self.var]:
			block = SpriteNode('pzl:Yellow3', 
								position=(x + pos[0], y + pos[1]), 
								color=colors[self.shapes.index(self.shape)],
								size=(side, side))
			self.figure.append(block)
			
					
	def move_down(self):
		for block in self.figure:
			y = block.position.y - side
			block.position = Point(block.position.x, y) 
		
				
	def left_right(self):
		for block in self.figure:
			for b in grounded_blocks:
				#to check if there's a block to the right at the same height. if yes, the block can't move right
				if block.position.y == b.position.y:
					if block.position.x + side == b.position.x:
						self.RIGHT = False
					if block.position.x - side == b.position.x:
						self.LEFT = False
		
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
		self.var += 1
		if self.var >= len(self.shape):
			self.var = 0
		
		#we need the cur position of the figure - any block in it
		x, y = self.figure[0].position	
		#take a block in self.figure and put it in a tuple with list where written how to move the block
		move_to = list(zip(self.figure, self.shape[self.var]))
		
		#move_to is smth like that: [(<_scene2.SpriteNode object at 0x114c33138>, [0, 0]), (<_scene2.SpriteNode object at 0x11366cae8>, [-34, 0])]
		for m in move_to:
			m[0].position = Point(m[1][0] + x, m[1][1] + y)
			
		for block in self.figure:
			if block.position.x > 153:
				for block in self.figure:
					x = block.position.x - side
					block.position = Point(x, block.position.y)
				
	
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
		if self.seconds > 0.2:
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
