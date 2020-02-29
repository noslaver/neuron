from PIL import Image

#def parse_color_image(context, snapshot):
#    ci = snapshot.color_image
#    image = Image.new('RGB', (ci.width, ci.height))
#    it = iter(ci.content)
#    image.putdata(list(zip(it, it, it)))
#    path = context.path('color_image.jpg')
#    image.save(path)

class ColorImageParser:
    def parse(self, context, snapshot):
        ci = snapshot.color_image
        image = Image.new('RGB', (ci.width, ci.height))
        it = iter(ci.content)
        image.putdata(list(zip(it, it, it)))
        path = context.path('color_image.jpg')
        image.save(path)
