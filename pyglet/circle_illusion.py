from pyglet.gl import *
from math import pi, sin, cos

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500


class MovingCircle(object):

    def __init__(self, x0, y0, radius, traj_angle,
                 traj_center_x=WINDOW_WIDTH/2., traj_center_y=WINDOW_HEIGHT/2., traj_length=WINDOW_WIDTH):
        self.x = x0
        self.y = y0
        self.radius = radius

        self.traj_center_x = traj_center_x
        self.traj_center_y = traj_center_y
        self.traj_angle = traj_angle
        self.traj_length = traj_length

        self.end1_x = self.traj_center_x - ((self.traj_length / 2.) - self.radius) * cos(self.traj_angle * pi / 180.)
        self.end1_y = self.traj_center_y - ((self.traj_length / 2.) - self.radius) * sin(self.traj_angle * pi / 180.)
        self.end2_x = self.traj_center_x + ((self.traj_length / 2.) - self.radius) * cos(self.traj_angle * pi / 180.)
        self.end2_y = self.traj_center_y + ((self.traj_length / 2.) - self.radius) * sin(self.traj_angle * pi / 180.)

        self.vx = (self.end2_x - self.end1_x) / 100.
        self.vy = (self.end2_y - self.end1_y) / 100.

    def draw(self):
        draw_full_circle(self.x, self.y, self.radius)

    def update_position(self, t):
        # TODO: encode position of ball in a "droite paramétrique" instead
        new_x = self.x + self.vx * t
        new_y = self.y + self.vy * t

        if new_x < self.end1_x or new_x > self.end2_x:
            self.vx *= -1.
            new_x = self.x + self.vx * t

        if new_y < self.end1_y or new_y > self.end2_y:
            self.vy *= -1.
            new_y = self.y + self.vy * t

        self.x = new_x
        self.y = new_y
        print(self.x)



def draw_full_circle(x, y, radius):
    """
    We want a pixel perfect circle. To get one, we have to approximate it densely with triangles.
    Each triangle thinner than a pixel is enough to do it.
    Sin and cosine are calculated once and then used repeatedly to rotate the vector.
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
        # point 1
        (WINDOW_WIDTH / 2.) - length * cos((angle - width) * pi / 180.),
        (WINDOW_WIDTH / 2.) - length * sin((angle - width) * pi / 180.),
        # point 2
        (WINDOW_WIDTH / 2.) - length * cos((angle + width) * pi / 180.),
        (WINDOW_WIDTH / 2.) - length * sin((angle + width) * pi / 180.),
        # point 3
        (WINDOW_WIDTH / 2.) + length * cos((angle - width) * pi / 180.),
        (WINDOW_WIDTH / 2.) + length * sin((angle - width) * pi / 180.),
        # point 4
        (WINDOW_WIDTH / 2.) + length * cos((angle + width) * pi / 180.),
        (WINDOW_WIDTH / 2.) + length * sin((angle + width) * pi / 180.),
    ]))


# function that increments the angle
t = 0
def update_frame(x, y):
    global t
    t += 1


if __name__ == "__main__":
    # creates window
    window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)


    @window.event
    def on_draw():
        # clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # draws the background circle
        glColor3f(0.5, 0., 0.)
        draw_full_circle(WINDOW_WIDTH / 2., WINDOW_HEIGHT / 2., WINDOW_WIDTH / 2.)

        # draws the moving circles
        glColor3f(1., 1., 1.)
        circle1 = MovingCircle(x0=WINDOW_WIDTH / 2., y0=WINDOW_HEIGHT / 2., radius=15., traj_angle=67.5)
        circle1.update_position(t)
        circle1.draw()

        # draws the bars
        glColor3f(0., 0., 0.)
        bar_width = 0.1
        angles = [0., 22.5, 45., 67.5, 90., 112.5, 135., 157.5]
        for angle in angles:
            draw_full_rectangle(WINDOW_WIDTH, width=bar_width, angle=angle)


    # every 1/10 th get the next angle
    pyglet.clock.schedule(update_frame, WINDOW_WIDTH / 2.)
    pyglet.app.run()
