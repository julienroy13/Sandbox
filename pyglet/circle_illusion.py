from pyglet.gl import *
from math import pi, sin, cos

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

def draw_full_circle(x, y, radius):
    """
    We want a pixel perfect circle. To get one,
    we have to approximate it densely with triangles.
    Each triangle thinner than a pixel is enough
    to do it. Sin and cosine are calculated once
    and then used repeatedly to rotate the vector.
    I dropped 10 iterations intentionally for fun.
    """
    iterations = int(2 * radius * pi)
    s = sin(2 * pi / iterations)
    c = cos(2 * pi / iterations)

    dx, dy = radius, 0.

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for _ in range(iterations + 1):
        glVertex2f(x + dx, y + dy)
        dx, dy = (dx * c + dy * s), (dy * c - dx * s)
    glEnd()


def draw_full_rectangle(length, width, angle):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [
        (WINDOW_WIDTH / 2.) - length * cos((angle - width) * pi / 180.), (WINDOW_WIDTH / 2.) - length * sin((angle - width) * pi / 180.),  # point 1
        (WINDOW_WIDTH / 2.) - length * cos((angle + width) * pi / 180.), (WINDOW_WIDTH / 2.) - length * sin((angle + width) * pi / 180.),  # point 2
        (WINDOW_WIDTH / 2.) + length * cos((angle - width) * pi / 180.), (WINDOW_WIDTH / 2.) + length * sin((angle - width) * pi / 180.),  # point 3
        (WINDOW_WIDTH / 2.) + length * cos((angle + width) * pi / 180.), (WINDOW_WIDTH / 2.) + length * sin((angle + width) * pi / 180.),  # point 4
        ]))


# function that increments the angle
frame = 0
def update_frame(x, y):
    global frame
    frame += 1


if __name__ == "__main__":
    # creates window
    window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

    @window.event
    def on_draw():
        # clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # draws the background of the clock (a missing triangle is used for seconds)
        glColor3f(0.5, 0., 0.)
        draw_full_circle(WINDOW_WIDTH / 2., WINDOW_HEIGHT / 2., WINDOW_WIDTH / 2.)

        # draws the bars
        glColor3f(0., 0., 0.)
        bar_width = 0.15
        angles = [0., 22.5, 45., 67.5, 90., 112.5, 135., 157.5]
        for angle in angles:
            draw_full_rectangle(WINDOW_WIDTH, width=bar_width, angle=angle)

    # every 1/10 th get the next angle
    pyglet.clock.schedule(update_frame, WINDOW_WIDTH / 2.)
    pyglet.app.run()
