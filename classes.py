import pygame as pg

pg.init()


class Widget:
    def __init__(self):
        self.id = None
        self.hidden = False
        self.pos = (0, 0)


class TextBox(Widget):
    def __init__(
        self, text, size, pos, color, actveColor, bgColor, outlineColor, font, fsize
    ):
        super().__init__()
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.bgColor = bgColor
        self.outlineColor = outlineColor
        self.activeColor = actveColor
        self.fsize = fsize
        self.font_name = font
        self.font = pg.font.SysFont(self.font_name, self.fsize)
        self.render = self.font.render(self.text, True, self.color)
        self.rect = pg.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.txt_rect = self.render.get_rect(midleft=self.rect.midleft)
        self.active = False
        self.link = None
        self.numbers_only = False

    def draw(self, screen):
        pg.draw.rect(
            screen, self.activeColor if self.active else self.bgColor, self.rect
        )
        pg.draw.rect(screen, self.outlineColor, self.rect.inflate(2, 2), 2)
        screen.blit(self.render, self.txt_rect)

    def set_text(self, text):
        self.text = text
        self.render = self.font.render(self.text, True, self.color)
        self.txt_rect = self.render.get_rect(midleft=self.rect.midleft)

    def set_pos(self, pos):
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def set_color(self, *, color, bgColor, outlineColor):
        self.color = color
        self.bgColor = bgColor
        self.outlineColor = outlineColor
        self.render = self.font.render(self.text, True, self.color)

    def set_font(self, font):
        self.font = font
        self.font = pg.font.SysFont(self.font, self.fsize)
        self.render = self.font.render(self.text, True, self.color)

    def set_size(self, size):
        self.fsize = size
        self.font = pg.font.SysFont(self.font, self.fsize)
        self.render = self.font.render(self.text, True, self.color)

    def check_click(self, app):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            for widget in app.widgets:
                if isinstance(widget, TextBox):
                    widget.active = False
            self.active = True

    def get_text(self):
        return self.text


class Image(Widget):
    def __init__(self, image, pos):
        super().__init__()
        self.image = pg.image.load(image)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_image(self, image):
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def set_pos(self, pos):
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Button(Widget):
    def __init__(self, text, pos, color, bgColor, outlineColor, font, size, action):
        super().__init__()
        self.text = text
        self.pos = pos
        self.color = color
        self.bgColor = bgColor
        self.outlineColor = outlineColor
        self.font = font
        self.size = size
        self.action = action
        self.font = pg.font.SysFont(self.font, self.size)
        self.render = self.font.render(self.text, True, self.color)
        self.rect = self.render.get_rect().inflate(10, 10)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.txt_rect = self.render.get_rect(center=self.rect.center)

    def draw(self, screen):
        pg.draw.rect(screen, self.bgColor, self.rect)
        pg.draw.rect(screen, self.outlineColor, self.rect.inflate(2, 2), 2)
        screen.blit(self.render, self.txt_rect)

    def set_text(self, text):
        self.text = text
        self.render = self.font.render(self.text, True, self.color)
        self.rect = self.render.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def set_pos(self, pos):
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def set_color(self, color):
        self.color = color
        self.render = self.font.render(self.text, True, self.color)

    def set_font(self, font):
        self.font = font
        self.font = pg.font.SysFont(self.font, self.size)
        self.render = self.font.render(self.text, True, self.color)

    def set_size(self, size):
        self.size = size
        self.font = pg.font.SysFont(self.font, self.size)
        self.render = self.font.render(self.text, True, self.color)

    def check_click(self, app):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.action:
                self.action()


class Label(Widget):
    def __init__(self, text, pos, color, font, size):
        super().__init__()
        self.text = text
        self.pos = pos
        self.color = color
        self.font = font
        self.size = size
        self.font = pg.font.SysFont(self.font, self.size)
        self.render = self.font.render(self.text, True, self.color)
        self.rect = self.render.get_rect(topleft=self.pos)

    def draw(self, screen):
        screen.blit(self.render, self.rect)

    def set_text(self, text):
        self.text = text
        self.render = self.font.render(self.text, True, self.color)
        self.rect = self.render.get_rect(topleft=self.pos)

    def set_pos(self, pos, wrt="topleft"):
        exec(f"self.rect.{wrt} = pos")
        self.pos = self.rect.topleft

    def set_color(self, color):
        self.color = color
        self.render = self.font.render(self.text, True, self.color)

    def set_font(self, font):
        self.font_name = font
        self.font = pg.font.SysFont(self.font_name, self.size)
        self.render = self.font.render(self.text, True, self.color)

    def set_size(self, size):
        self.size = size
        self.font = pg.font.SysFont(self.font_name, self.size)
        self.render = self.font.render(self.text, True, self.color)
