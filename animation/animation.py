class Animation:
    def __init__(self, images, animation_speed=5, loop=True):
        self._images = images
        self._loop = loop
        self._animation_speed = animation_speed
        self._done = False
        self._frame = 0

    def copy(self):
        return Animation(self._images, self._animation_speed, self._loop)

    def length(self):
        return len(self._images)

    def update(self, dt):
        if self._loop:
            self._frame += self._animation_speed * dt
        else:
            self._frame = min(self._frame + self._animation_speed * dt, self.length() - 1)
            if self._frame >= self.length() - 1:
                self._done = True

    def img(self):
        return self._images[int(self._frame % (self.length()))]


class SetAnimation:
    def __init__(self, images, loop=True):
        self.images = images
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return SetAnimation(self.images, self.loop)

    def length(self):
        return len(self.images)

    def update(self, dt, frame):
        self.frame = frame

    def img(self):
        return self.images[int(self.frame % (self.length() - 1))]
