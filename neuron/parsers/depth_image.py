import matplotlib.pyplot as plt
import numpy as np


def parse_depth_image(context, snapshot):
    image = snapshot.depth_image
    with open(image.path, 'rb') as reader:
        content = reader.read()
        image = np.reshape(content, (image.width, image.height))
        plt.imshow(image, cmap='hot', interpolation='nearest')
        plt.savefig(context.directory / 'depth_image.png')


parse_depth_image.field = 'depth_image'
