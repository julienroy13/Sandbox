import cocos
import numpy as np
import os
import argparse
import pyglet

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

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

    def __init__(self, args):
        super().__init__()

        # Creates a sprite
        self.sprite = cocos.sprite.Sprite('ball.png')
        self.sprite.position = 500, 500
        self.sprite.scale = 0.5

        # Adds the sprite to our layer (z is its position in an axis coming out of the screen)
        self.add(self.sprite, z=1)
        
        self.window_width = args.width
        self.window_height = args.height

    def update_ball_position(self, dx, dy):
        new_position_x = self.sprite.x + dx
        new_position_y = self.sprite.y + dy
        if new_position_x - self.sprite.width//2 > 0 and new_position_x + self.sprite.width//2 < self.window_width:
            self.sprite.x += dx
        if new_position_y - self.sprite.height//2 > 0 and new_position_y + self.sprite.height//2 < self.window_height:
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

        # Checks if mouse is in the circle
        if ((x - self.sprite.x)**2 + (y - self.sprite.y)**2 < (self.sprite.width//2)**2):
            self.update_ball_position(dx, dy)

def args_check(args):
    """
    Just takes our args as input, manually check some conditions
    :param args: args
    :return: args
    """
    if args.width < 50 or args.width > 2000:
        raise ValueError(f'Parameter "args.width" should be between 50 and 2000. Got {args.width} instead')

    if args.height < 50 or args.height > 1000:
        raise ValueError(f'Parameter "args.height" should be between 50 and 1000. Got {args.height} instead')

    return args


if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', default=DEFAULT_WIDTH)
    parser.add_argument('--height', default=DEFAULT_HEIGHT)
    args = args_check(parser.parse_args())

    # Initializes the director (whatever this does)
    cocos.director.director.init(width=args.width, height=args.height, caption='Bouncing Ball', resizable=True)

    # Instantiates our layer and creates a scene that contains our layer as a child
    main_scene = cocos.scene.Scene(Background(), BouncingBall(args))

    # We run our scene
    cocos.director.director.run(main_scene)