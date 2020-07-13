import scene
import sound


def sw(): return scene.get_screen_size()[0]
def sh(): return scene.get_screen_size()[1]
def bw(): return 100
def bh(): return 100

right = left = down = up = None

icons = {
	     'iob:arrow_down_b_256' : (sw()/4*3, 60),
	     'iob:arrow_up_b_256' : (sw()/4*3, bh() + 60),
	     'iob:arrow_left_b_256' : (sw()/4*3 - 95, bh()),
	     'iob:arrow_right_b_256' : (sw()/4*3 + 95, bh())
	      }


class Arrow(ShapeNode):
	def __init__(self,
				 icon,
				 path=None,
	             size=Size(120, 120),
	             corner_radius=8,
	             border_size=20,
	             borderColor='#3f0917',
	             position=(0,0),
	             parent=None,
	             *args, **kwargs):
	             	
	             	#for border
	             	self.icon = icon
	             	self.corner_radius = corner_radius
	             	self.border_size = border_size
	             	self.borderColor = borderColor
	             	
	             	self.position = position
	             	self.size = size
	             	
	             	#for super()
	             	self.x, self.y = position
	             	self.w, self.h = size
	             	
	             	super().__init__(fill_color='white',
	             					path=ui.Path.rounded_rect(self.x, 
	             											   self.y,
	             											   self.w/1.5, 
	             											   self.h/1.5,
	             											   self.corner_radius),
	             					stroke_color=borderColor,
	             					parent=parent,
	             					*args, **kwargs)
	             					
	             	self._setup(self.icon)
	             	                 
	def _setup(self, i):
		if self.icon:
			arrow = SpriteNode(self.icon,
							   position=Point(0, 0), 
							   size=(100, 100),
							   parent=self)
							   
	             	                 

class Main(Scene):            	                 
	def setup(self):
		fill_color = self.background_color
		self.background_color = 'white'
		self.arrows = [Arrow(i, position=icons[i], parent=self) for i in icons] 
			
			
	def touch_began(self, touch):
		tapped = True
		for arw in self.arrows:
			if touch.location in arw.frame:
				sound.play_effect('rpg:Chop')
				arw.fill_color = '#969696'
				
			
	def touch_ended(self, touch):
		for arw in self.arrows:
			if arw.fill_color == '#969696':
				arw.fill_color = 'white'
				right = left = down = up = None
				
		
				
if __name__ == '__main__':				
	run(Main(), PORTRAIT)
