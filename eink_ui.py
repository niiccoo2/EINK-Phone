from PIL import Image, ImageDraw

class EInkUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new('1', (width, height), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.components = []

    def add(self, component):
        self.components.append(component)

    def draw_all(self):
        self.image.paste(255, [0, 0, self.width, self.height])  # Clear to white
        for c in self.components:
            c.draw(self.draw)

    def get_image(self):
        return self.image
