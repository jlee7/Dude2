#-*-coding:utf8;-*-
#qpy:2
#qpy:kivy
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.core.window import Window
from kivy.clock import Clock
from random import random
import math
# Own imports
from characters import Dude, GoodItem, BadItem, ScoreLabel


class Game(Widget):
    """This Widget hosts the game. Touch inputs are processed."""
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.is_running = True

        # Create the dude
        self.dude = Dude()
        self.add_widget(self.dude)

        # Create the good and bad items
        for n in range(10):
            self.add_widget(GoodItem())

        for n in range(10):
            self.add_widget(BadItem())

        # Set variable for initial touch coordinates
        self.init_touch_x = None
        self.init_touch_y = None

        # Set Label at the end, because it interferes with dude and items
        self.lbl_points = ScoreLabel()
        self.add_widget(self.lbl_points)

    def start_game(self):
        """Starts the game by starting the clock"""
        self.game_clock = Clock.schedule_interval(self.my_callback, 1/60)
        #Clock.schedule_interval(self.my_callback, 1/60)

    def stop_game(self):
        """Stops the game by stopping the clock. Clears the canvas."""
        Clock.unschedule(self.game_clock)
        self.popup = Popup(title="Game Over",
                           #content=Label(text=("Score: " + str(self.lbl_points.score))),
                           content=Button(text="Score: " + str(self.lbl_points.score) + "\nPress me", 
                                          on_release=self.on_btn_finish),
                           size_hint=(0.4, 0.2),
                           auto_dismiss=False)
        

        self.popup.open()
        
    def on_btn_finish(self, event):
        # Note to myself:
        # If Dude and Label are not removed at the end, they will stay on the canvas.
        # They will be invisible and check_if_dude_alone() will not work.
        # Everything is going to be rebuilt by reset_game(). Screen chanes.
        self.children = []

        self.canvas.clear()
        # Reset the game
        self.reset_game()
        self.popup.dismiss()

        # Remove the Finish button from parent.
        #self.parent.remove_widget(self.btn_finish)

        # Change the screen
        self.parent.manager.current = "end"

    def reset_game(self):
        """Resets the game by recreating all game objects in the same order."""

        self.dude = Dude()
        self.add_widget(self.dude)

        for n in range(10):
            self.add_widget(GoodItem())

        for n in range(10):
            self.add_widget(BadItem())
        self.init_touch_x = None
        self.init_touch_y = None

        self.lbl_points = ScoreLabel()
        self.add_widget(self.lbl_points)

    def on_touch_down(self, touch):
        """Gets the initial touch and draws image on that spot."""
        print("Touch down")
        self.init_touch_x = touch.x
        self.init_touch_y = touch.y
        self.init_touch_pos = (touch.x, touch.y)
        print("Initial touch:", self.init_touch_x, self.init_touch_y)

        # Instructions what to draw
        with self.canvas:
            d = 30.
            Ellipse(source="graphics/move.png",pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))

    def on_touch_move(self, touch):
        """Gets the vector by triggering self.calculate_vector() and 
           passes it to Dude's set_move() method. Using "try", because Exception
           raises when (not initial) touch.pos holds a 0"""
        try:
            vector = self.calculate_vector(self.init_touch_pos, touch.pos)
            self.dude.set_move(vector[0],vector[1])
        except Exception as e:
            print(e)

    def on_touch_up(self, touch):
        """Removes the image drawn by self.on_touch_down()."""
        
        # Sets the vector to zero, so dude does not move anymore.
        self.dude.set_move(0, 0)
        
        # Removes the Ellipse with the image
        for child in self.canvas.children:
            if type(child) == Ellipse:
                self.canvas.remove(child)

    def calculate_vector(self, init_point, second_point):
        """http://stackoverflow.com/questions/17332759/finding-vectors-with-2-points"""
        distance = [second_point[0] - init_point[0], second_point[1] - init_point[1]]
        norm = math.sqrt(distance[0]**2 + distance[1]**2)
        direction = [distance[0]/norm, distance[1]/norm]

        return direction

    def my_callback(self, event):
        """Update function which is bind to the Clock module.
           Makes dude move a little each time and checks collision.
           Also checks, if dude has no more to eat."""
        self.dude.check_move()
        self.check_collision()
        self.check_if_dude_alone()

    def check_if_dude_alone(self):
        """Checks if only Dude and Label are left"""
        if len(self.children) <= 2:
            self.stop_game()
            print("Dude is alone.")

    def update_score(self, item):
        self.lbl_points.score += item.value

    def check_collision(self):
        """Checks collisions and triggers removal and points."""
        for child in self.children:
            if type(child) != Dude:
                if self.dude.collide_widget(child):
                    #print("Dude collides with", child)
                    if self.dude.collision_event(child):
                        self.update_score(child)
                        self.remove_widget(child)
                        #self.lbl_points.score += 5
                    else:
                        print("collision, but no removal")


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.name = "game"
        self.game = Game()
        self.add_widget(self.game)
        self.size = Window.size
        print("GameScreen size:", self.size)

    def on_enter(self):
        self.game.start_game()

    def on_leave(self):
        #self.game.stop_game()
        #self.game.reset_game()
        #self.manager.current = "end"
        pass

class EndScreen(Screen):
    def __init__(self, **kwargs):
        super(EndScreen, self).__init__(**kwargs)
        self.name = "end"
        self.frame = BoxLayout(orientation="vertical")
        self.btn_start = Button(text="Go to Start Screen")
        self.btn_start.bind(on_release=self.to_startscreen)
        self.frame.add_widget(self.btn_start)

        self.btn_quit = Button(text="QUIT")
        self.btn_quit.bind(on_release=self.quit)
        self.frame.add_widget(self.btn_quit)

        self.add_widget(self.frame)

    def to_startscreen(self, event):
        self.manager.current = "start"

    def quit(self, event):
        exit()

    def on_enter(self):
        pass

    def on_leave(self):
        pass

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.name = "start"
        self.frame = BoxLayout(orientation="vertical")
        self.btn_start = Button(text="START")
        self.btn_start.bind(on_release=self.start)
        self.frame.add_widget(self.btn_start)

        self.btn_quit = Button(text="QUIT")
        self.btn_quit.bind(on_release=self.quit)
        self.frame.add_widget(self.btn_quit)

        self.add_widget(self.frame)

    def start(self, event):
        print("STARTING GAME")
        self.manager.current = "game"


    def quit(self, event):
        exit()

class GameApp(App):

    def build(self):
        # Create Screens
        self.screenmanager = ScreenManager()
        self.startscreen = StartScreen()
        self.game_screen = GameScreen()
        self.end_screen = EndScreen()

        # Add widgets to their parents
        self.screenmanager.add_widget(self.startscreen)
        self.screenmanager.add_widget(self.game_screen)
        self.screenmanager.add_widget(self.end_screen)
        
        print(self.screenmanager.current)
        return self.screenmanager

if __name__ == "__main__":
    #Window.size = (720,1200)
    Window.size = (360, 600)
    #Window.size = (600, 360)
    GameApp().run()



"""
Useful Information:
Positioning Widgets: https://blog.kivy.org/2014/10/updating-canvas-instructions-declared-in%C2%A0python/


Icons made by 
Pixel Buddha
fromwww.flaticon.com
is licensed by CC 3.0 BY
"""