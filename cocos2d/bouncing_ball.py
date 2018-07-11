import cocos
import numpy as np
import os
import argparse
import pyglet

class Background(cocos.layer.ColorLayer):
    # If you want that your layer receives director.window events, you must set this variable to 'True'
    is_event_handler = True

    def __init__(self):
        # blueish color
        super().__init__(0, 51, 153, 255)

        # Creates a label to display text
        label = cocos.text.Label(
            'Bouncing Ball',
            font_name='Calibri',
            font_size=32,
            anchor_x='center', anchor_y='center',
            position=((320, 240))
        )

        # Adds the label (which is a subclass of CocosNode) as a child of our layer node
        self.add(label)


class BouncingBall(cocos.layer.Layer):
    # If you want that your layer receives director.window events, you must set this variable to 'True'
    is_event_handler = True

    def __init__(self):
        super().__init__()

        # Creates a sprite
        self.sprite = cocos.sprite.Sprite('ball.png')
        self.sprite.position = 500, 500
        self.sprite.scale = 0.5

        # Adds the sprite to our layer (z is its position in an axis coming out of the screen)
        self.add(self.sprite, z=1)

    def update_ball_position(self, dx, dy):
        self.sprite.x += dx
        self.sprite.y += dy

    # EVENT HANDLERS
    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed.
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise-or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
        """
        key_name = pyglet.window.key.symbol_string(key)
        if key_name == 'LEFT':
            self.update_ball_position(-1, 0)
        elif key_name == 'RIGHT':
            self.update_ball_position(1, 0)
        elif key_name == 'UP':
            self.update_ball_position(0, 1)
        elif key_name == 'DOWN':
            self.update_ball_position(0, -1)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Called when the mouse moves over the app window with some button(s) pressed
        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the last call.
        'buttons' is a bitwise-or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise-or of pyglet.window.key modifier constants (values like 'SHIFT', 'OPTION', 'ALT')
        """
        # TODO : Improve to make it so that the circle condition is a circle, not a square
        mouse_in_circle_x = x > (self.sprite.x - self.sprite.width//2) and x < (self.sprite.x + self.sprite.width//2)
        mouse_in_circle_y = y > (self.sprite.y - self.sprite.height//2) and y < (self.sprite.y + self.sprite.height//2)
        if mouse_in_circle_x and mouse_in_circle_y:
            self.update_ball_position(dx, dy)

def args_check(args):
    """
    Just takes our args as input, manually check some conditions
    :param args: args
    :return: args
    """
    pass

    return args


if __name__ == '__main__':
    # Parse args
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--tuto', default=DEFAULT_TUTO)
    # args = args_check(parser.parse_args())

    # Initializes the director (whatever this does)
    cocos.director.director.init(width=1280, height=720, caption='Bouncing Ball', resizable=True)

    # Instantiates our layer and creates a scene that contains our layer as a child
    main_scene = cocos.scene.Scene(Background(), BouncingBall())

    # We run our scene
    cocos.director.director.run(main_scene)