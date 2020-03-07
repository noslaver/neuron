import matplotlib.pyplot as plt
import numpy as np
import struct


def parse_depth_image(context, snapshot):
    image = snapshot.depth_image
    with open(image.path, 'rb') as reader:
        content = reader.read()
        content = struct.unpack(f'{image.width * image.height}f', content)
        image = np.reshape(content, (image.width, image.height))
        plt.imshow(image, cmap='hot', interpolation='nearest')
        path = context.path('depth_image.png')
        plt.savefig(path)

        return {'parsed_image_path': str(path)}


parse_depth_image.field = 'depth_image'
