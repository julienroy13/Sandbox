from pyglet.gl import *
from math import pi, sin, cos
import numpy as np

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

CARTESIAN_LIMIT = 1


def cartesian_to_window(point):
    x, y = point
    return [(x + CARTESIAN_LIMIT) * WINDOW_WIDTH / (2 * CARTESIAN_LIMIT),
            (y + CARTESIAN_LIMIT) * WINDOW_HEIGHT / (2 * CARTESIAN_LIMIT)]


def make_circle(x, y, radius, frame):
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

    dx, dy = radius * cos(frame / 100.), radius * sin(frame / 100.)

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for _ in range(iterations + 1 - 10):
        glVertex2f(x + dx, y + dy)
        dx, dy = (dx * c - dy * s), (dy * c + dx * s)
    glEnd()


# get all the points in a circle centered at 0.
def PointsInCircum(r, n=25):
    return [(cos(2 * pi / n * x) * r, sin(2 * pi / n * x) * r) for x in range(0, n + 1)]

pts = np.array(PointsInCircum(WINDOW_WIDTH/2.))

# function that increments the frame
frame = 0
def update_frame(x, y):
    global frame
    frame += 1


if __name__ == "__main__":
    # creates window
    window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

    # creates fps display
    fps_display = pyglet.clock.ClockDisplay()

    @window.event
    def on_draw():
        # clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(0, 0, 0.5)
        make_circle(WINDOW_WIDTH / 2., WINDOW_HEIGHT / 2., WINDOW_WIDTH / 2., frame)

        glColor3f(0, 0, 0.)
        # draw the next line
        # in the circle animation
        # circle centered at 100,100,0 = x,y,z
        glBegin(GL_LINES)
        glVertex3f(250, 250, 0)
        glVertex3f(pts[frame % pts.shape[0]][1] + 250, pts[frame % pts.shape[0]][0] + 250, 0)
        glEnd()

        # draws fps display
        fps_display.draw()


    # every 1/10 th get the next frame
    pyglet.clock.schedule(update_frame, 100.)
    pyglet.app.run()
