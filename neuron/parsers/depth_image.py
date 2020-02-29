import matplotlib.pyplot as plt
import numpy as np


def parse_depth_image(context, snapshot):
    image = snapshot.depth_image
    image = np.reshape(image.content, (image.width, image.height))
    plt.imshow(image, cmap='hot', interpolation='nearest')
    plt.savefig(context.directory / 'depth_image.png')
