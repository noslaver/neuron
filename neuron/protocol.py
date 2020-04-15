class Image:
    def __init__(self, ty, height, width, image_path):
        self.type = ty
        self.height = height
        self.width = width
        self.image_path = image_path

    def __str__(self):
        return f'{self.width}x{self.height} {self.type} image'

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.type} {self.width}x' + \
               f'{self.height}>'


class Feelings:
    def __init__(self, hunger, thirst, exhaustion, happiness):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness


class Pose:
    def __init__(self, translation, rotation):
        self.translation = translation
        self.rotation = rotation


class Snapshot:
    def __init__(self, timestamp, pose, color_image, depth_image, feelings):
        self.timestamp = timestamp
        self.pose = pose
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __str__(self):
        return f'Snapshot from {self.timestamp} on {self.pose.translation}' + \
               f' / {self.pose.rotation}, ' + f'with a {self.color_image} ' + \
               f'and a {self.depth_image}.'
