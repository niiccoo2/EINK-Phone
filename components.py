class Label:
    def __init__(self, x, y, text, size=12):
        self.x = x
        self.y = y
        self.text = text
        self.size = size

    def draw(self, draw):
        draw.text((self.x, self.y), self.text, fill=0)
