from basewidget import WidgetDrawer
from random import randrange
from kivy.properties import NumericProperty
from kivy.core.window import Window

from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color


# Character Class
class Dude(WidgetDrawer):
    """The Dude. You know it when you see him."""
    def __init__(self, **kwargs):
        self.image = "graphics/party-dude.png"
        self.pos = (Window.size[0] / 2 - self.size[0] / 2, 0)
        self.size = [Window.size[0] / 7, Window.size[0] / 7]
        self.move_x = 0
        self.move_y = 0
        self.speed = Window.size[0] / 50
        super(Dude, self).__init__(imageStr=self.image, image_size=self.size , **kwargs)


    def set_move(self, xpos, ypos):
        """This sets the vector components."""
        self.move_x = xpos
        self.move_y = ypos

    def check_move(self):
        """Checks if move is inside Window."""
        if self.x <= 0 and self.move_x < 0\
        or self.x >= Window.size[0] and self.move_x > 0:
            print("Target X outside window.")
        else:
            self.move_on_x_axis()

        if self.y <= 0 and self.move_y < 0\
        or self.y >= Window.size[1] and self.move_y > 0:
            print("Target Y outside window.") 
        else:
            self.move_on_y_axis()

        #print(Window.size, self.x, self.y)

    def move_on_x_axis(self):
        """Move on x axis"""
        self.x += self.move_x * self.speed
        
    def move_on_y_axis(self):
        """Move on y axis"""
        self.y += self.move_y * self.speed

    def collision_event(self, collision_object):
        """returns True to remove collision object, 
                   False to keep collision_object"""
        if type(collision_object) == GoodItem:
            self.size[0] += 5
            self.size[1] += 5
            print("Dude grows to", self.size)
            return True
        elif type(collision_object) == BadItem:
            self.size[0] -= 5
            self.size[1] -= 5
            print("Dude shrinks to", self.size)
            return True
        elif type(collision_object) == ScoreLabel:
            print("Dude collides with Label. Label will not be removed.")
            return False
        else:
            print("Unknown action for:", collision_object)
            return True



class GoodItem(WidgetDrawer):
    def __init__(self, **kwargs):
        self.image = "graphics/item-six-pack_green.png"
        self.size = [Window.size[0] / 15, Window.size[0] / 15]
        super(GoodItem, self).__init__(imageStr=self.image, image_size=self.size , **kwargs)
        self.pos = (randrange(10, Window.size[0] - self.size[0]), 
                    randrange(10, Window.size[1] - self.size[1] * 3))
        self.value = 10


class BadItem(WidgetDrawer):
    def __init__(self, **kwargs):
        self.image = "graphics/item-book_red.png"
        self.size = [Window.size[0] / 15, Window.size[0] / 15]
        super(BadItem, self).__init__(imageStr=self.image, image_size=self.size , **kwargs)
        self.pos = (randrange(10, Window.size[0] - self.size[0]), 
                    randrange(10, Window.size[1] - self.size[1] * 3))
        self.value = -5


class ScoreLabel(Label):
    def __init__(self, **kwargs):
        super(ScoreLabel, self).__init__(**kwargs)
        self.size = (Window.size[0], Window.size[1] / 10)
        self.y = Window.size[1] - self.size[1]

        # Create custom property and bind a callback
        self.create_property("score")
        self.score = 0
        self.bind(score=self.update_score)

        # Needs to be after the created property
        self.text = str(self.score)
        # Set color of Label (text), this is not the background color
        #self.color = 1,0,0,1 

        # Draw the Image 
        with self.canvas.before:
            Rectangle(source="graphics/bg_score.png", pos=self.pos, size=self.size)

    def update_score(self, obj, value):
        print(obj, value)
        self.text = str(self.score)
        print(self.text, self.score)





        


