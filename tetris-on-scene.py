from scene import *
import random, sound
from arrows import *

sw, sh = get_screen_size()
rect_w = sw/3  #343.33
rect_h = 612 #668
side = int(rect_w/10) 
colors = ['red', 'orange', 'yellow']

grounded_blocks = []
rows = [0 for i in range(18)]
score = 0

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
							 
			self.score_label = None
			self.score_font = ('Avenir Next', 40)
		
	
	#called only once at Game's init. draws the score at the beginning when it's 0
	def draw_zero(self):
		self.score_label = LabelNode('0', font=self.score_font, 
							  color='black', position=(-rect_w/2, rect_h/2),
							  anchor_point=(0, 0), parent=self)
							  
	
	#removes the number of previous score and shows a new number					  
	def show_scores(self):
		self.score_label.remove_from_parent()
		self.score_label = LabelNode(str(score), font=self.score_font, 
							  color='black', position=(-rect_w/2, rect_h/2),
							  anchor_point=(0, 0), parent=self)
							  
							  
	def champion_portrait(self):
		champion = SpriteNode('IMG_0177.JPG', position=(sw/4*2 - 100, 80), 
							   size=(410, 350), parent=self)
		text = "Joseph Saelee, world's champion at tetris"
		
		explain = LabelNode(text, font=('Bradley Hand', 23), color='black',
		 					position=champion.position-(0, 200), parent=self)
		self.crown = SpriteNode('IMG_0181.JPG', position=champion.position+(-30, 230),
								size=(80, 80), parent=self)
								
		

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
				
			if block.position.x < -153:
				for block in self.figure:
					x = block.position.x + side
					block.position = Point(x, block.position.y)
					
	
	#list rows stores inf how many blocks are in every row			
	def put_in_row(self):
		for block in self.figure:
			global score
			score += 1
			#the lowest position.y of a block is -289
			row = int((block.position.y + 289)/side)
			rows[row] += 1
			delete_rows = []
		
		for n in range(len(rows)):
			if rows[n] == 10:
				delete_rows.append(n)
		combo = len(delete_rows)
		
		for n in delete_rows:
			self.delete_row(n, combo)
		if delete_rows:
			self.rows_down(combo)
			
					
	#the func deletes row if it's full and adds score for deleting the row
	def delete_row(self, n, combo):
		deleted = []
		y = n*side - 289
		#blocks of the full row disappear and are removed from grounded_blocks
		for b in grounded_blocks:
			if b.position.y == y:
				b.run_action(A.scale_to(0))
				deleted.append(b)
		print(len(grounded_blocks), 1)
				
		#remiving the deleted blocks from grounded_blocks		
		for block in deleted:
			grounded_blocks.pop(grounded_blocks.index(block))
		print(len(grounded_blocks), 2)
	
		global score		
		if combo == 1:
			score += 10
		elif combo != 1:
			score = combo*10 + 10 
			
			
	def rows_down(self, n):
		#blocks upper to the full row move down	
		y = n*side - 323
		for b in grounded_blocks:
			if b.position.y > y:
				b.run_action(A.move_by(0, -34*n))
				
		for r in range(len(rows)):
			if r == len(rows) - n:
				break
			else:
				rows[r] = rows[r+n]
		
	
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
		self.board.champion_portrait()
		
		self.seconds = 0
		self.figure = None
		self.faster = 1
		self.add_buttons()
		self.add_figure()
		self.grey_rect.draw_zero()
		
	
	def update(self):
		level = 1 + score/100
		self.seconds += self.dt
		if self.seconds > 0.3/(self.faster*level):
			self.seconds = 0
			if not self.figure.if_grounded():
				self.figure.move_down()
			else:
				for block in self.figure.figure:
					grounded_blocks.append(block)
				self.figure.put_in_row()
				self.grey_rect.show_scores()
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
					
				elif 'down' in arw.icon:
					self.faster = 3
			
	
	def touch_ended(self, touch):
		self.faster = 1
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
		
