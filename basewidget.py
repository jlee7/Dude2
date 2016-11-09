from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

class WidgetDrawer(Widget):
    """Adding the pos and size updates to Kivy's Widget class"""
    def __init__(self, imageStr, image_size, **kwargs): 
        super(WidgetDrawer, self).__init__(**kwargs)
        with self.canvas: 
            #setup a default size for the object
            self.size = image_size #(Window.width*.002*25,Window.width*.002*25) 
            #this line creates a rectangle with the image drawn on top
            self.rect_bg=Rectangle(source=imageStr,pos=self.pos,size = self.size) 
            #this line calls the update_graphics_pos function every time the position variable is modified
            self.bind(pos=self.update_graphics_pos)
            self.bind(size=self.update_graphics_size)  
            self.x = self.center_x
            self.y = self.center_y
            #center the widget 
            self.pos = (self.x,self.y) 
            #center the rectangle on the widget
            self.rect_bg.pos = self.pos 
 
    def update_graphics_pos(self, instance, value):
        #if the widgets position moves, the rectangle that contains the image is also moved
        self.rect_bg.pos = value

    def update_graphics_size(self, instance, value):
        #if the widgets position moves, the rectangle that contains the image is also moved
        self.rect_bg.size = value

    #use this function to change widget size        
    def setSize(self,width, height): 
        self.size = (width, height)
    #use this function to change widget position    
    def setPos(xpos,ypos):
        self.x = xpos
        self.y = ypos

"""
The WidgetDrawer class was taken from here:
https://kivyspacegame.wordpress.com/2014/06/20/flappy-ship-a-step-by-step-game-tutorial-part-1/
Canvas binding for "size" has been added.
"""
