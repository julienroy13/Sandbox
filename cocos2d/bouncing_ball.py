import cocos
import numpy as np
import os
import argparse
import pyglet
import logging

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
DEFAULT_GRAVITY_FORCE = 0.2

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
        self.sprite = cocos.sprite.Sprite('assets/ball.png')
        self.sprite.position = 500, 500  # arbitrary
        self.sprite.scale = 0.3          # arbitrary

        # Adds the sprite to our layer (z is its position in an axis coming out of the screen)
        self.add(self.sprite, z=1)

        self.window_width = args.width
        self.window_height = args.height

        self.velocity_x = 0.
        self.velocity_y = 0.

        self.sprite.color = (255, 255, 255)

        self.gravity_ON = True
        self.gravity_direction = 'DOWN'
        self.gravity_force = args.gravity_force

        self.is_holded = False

    def update_ball_position(self, dx, dy, new_dx=None, new_dy=None):
        new_position_x = self.sprite.x + dx
        new_position_y = self.sprite.y + dy

        # If the ball movement keeps it inside the screen, the ball's position is updated
        if new_position_x - self.sprite.width//2 > 0 and new_position_x + self.sprite.width//2 < self.window_width:
            self.sprite.x += dx
        else:
            # Else, the ball bounces
            self.velocity_x = -0.8 * self.velocity_x

        # ... same for y
        if new_position_y - self.sprite.height//2 > 0 and new_position_y + self.sprite.height//2 < self.window_height:
            self.sprite.y += dy
        else:
            self.velocity_y = -0.8 * self.velocity_y

        # If a new speed is provided, the ball's speed is updated
        if new_dx is not None:
            self.velocity_x = new_dx

        if new_dy is not None:
            self.velocity_y = new_dy


    # EVENT HANDLERS
    def on_mouse_release(self, x, y, buttons, modifiers):
        self.is_holded = False

    def on_mouse_press(self, x, y, buttons, modifiers):
        """This function is called when any mouse button is pressed
        (x, y) are the physical coordinates of the mouse
        'buttons' is a bitwise-or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise-or of pyglet.window.key modifier constants(values like 'SHIFT', 'OPTION', 'ALT')
        """
        # Checks if mouse is in the circle
        if ((x - self.sprite.x)**2 + (y - self.sprite.y)**2 < (self.sprite.width // 2)**2):
            self.is_holded = True


    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed.
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise-or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
        """
        key_name = pyglet.window.key.symbol_string(key)

        # Arrows keys select the orientation of the gravity
        if key_name in ['LEFT', 'RIGHT', 'DOWN', 'UP']:
            logging.info(f'{key_name}-key has been pushed. Gravity is now oriented towards {self.gravity_direction}')
            self.gravity_direction = key_name

        # Space-bar key turns off/on the gravity
        if key_name == 'SPACE':
            logging.info(f'SPACE-key has been pushed. Gravity is now {self.gravity_ON}')
            self.gravity_ON = not self.gravity_ON

        # Enter key sets the ball speed to zero
        if key_name == 'ENTER':
            logging.info(f"ENTER-key has been pushed. Ball's speed has been reset")
            self.velocity_x = 0.
            self.velocity_y = 0.


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Called when the mouse moves over the app window with some button(s) pressed
        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the last call.
        'buttons' is a bitwise-or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise-or of pyglet.window.key modifier constants (values like 'SHIFT', 'OPTION', 'ALT')
        """
        if self.is_holded:
            self.update_ball_position(dx, dy, new_dx=dx, new_dy=dy)


class EditLayer(cocos.layer.Layer):
    # is_event_handler = True
    # TODO : take into account the world coordinates vs window coordinates
    def __init__(self, ball):
        super().__init__()

        self.ball = ball

        self.schedule(self.update)

    def on_enter(self):
        super().on_enter()

    def update(self, dt):
        if self.ball.is_holded:
            self.ball.sprite.color = (120, 120, 120)
        else:
            self.ball.sprite.color = (255, 255, 255)

        # If the ball is holded, gravity does not affect it
        if self.ball.is_holded:
            self.ball.update_ball_position(0, 0, 0, 0)
        else:
            # At every frame update, the ball gains velocity in the negative direction of y
            if self.ball.gravity_ON:
                if self.ball.gravity_direction == 'DOWN':
                    self.ball.velocity_y -= self.ball.gravity_force
                elif self.ball.gravity_direction == 'UP':
                    self.ball.velocity_y += self.ball.gravity_force
                elif self.ball.gravity_direction == 'LEFT':
                    self.ball.velocity_x -= self.ball.gravity_force
                elif self.ball.gravity_direction == 'RIGHT':
                    self.ball.velocity_x += self.ball.gravity_force
                else:
                    raise ValueError(f'Unsupported gravity_direction : {self.ball.gravity_direction}')
            self.ball.update_ball_position(dx=self.ball.velocity_x, dy=self.ball.velocity_y)


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

    if args.gravity_force < 0.05 or args.gravity_force > 1.:
        raise ValueError(f'Parameter "args.gravity_force" should be between 0.05 and 1. Got {args.gravity_force} instead')

    return args


if __name__ == '__main__':
    # Basic logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S'
                        )

    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', default=DEFAULT_WIDTH)
    parser.add_argument('--height', default=DEFAULT_HEIGHT)
    parser.add_argument('--gravity_force', default=DEFAULT_GRAVITY_FORCE)
    args = args_check(parser.parse_args())

    # Initializes the director (whatever this does)
    cocos.director.director.init(width=args.width, height=args.height, caption='Bouncing Ball', resizable=True)

    # Instantiates our layer and creates a scene that contains our layer as a child
    background = Background()
    ball = BouncingBall(args)
    editor = EditLayer(ball)
    main_scene = cocos.scene.Scene(background, ball, editor)

    # We run our scene
    cocos.director.director.run(main_scene)