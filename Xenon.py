import pygame as pg
import sys  

pg.init()

class Widget:
    def __init__(self):
        self.id = None
        self.hidden = False
        self.pos = (0,0)

class TextBox(Widget):
    def __init__(self,text,size,pos,color,actveColor,bgColor,outlineColor,font,fsize):
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
        self.font = pg.font.SysFont(self.font_name,self.fsize)
        self.render = self.font.render(self.text,True,self.color)
        self.rect = pg.rect.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.txt_rect = self.render.get_rect(midleft = self.rect.midleft)
        self.active = False
        self.link = None
        self.numbers_only = False

    def draw(self,screen):
        pg.draw.rect(screen,self.activeColor if self.active else self.bgColor,self.rect)
        pg.draw.rect(screen,self.outlineColor,self.rect.inflate(2,2),2)
        screen.blit(self.render,self.txt_rect)
    
    def set_text(self,text):
        self.text = text
        self.render = self.font.render(self.text,True,self.color)
        self.txt_rect = self.render.get_rect(midleft = self.rect.midleft)


    def set_pos(self,pos):
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
    
    def set_color(self,*,color,bgColor,outlineColor):
        self.color = color
        self.bgColor = bgColor
        self.outlineColor = outlineColor
        self.render = self.font.render(self.text,True,self.color)

    def set_font(self,font):
        self.font = font
        self.font = pg.font.SysFont(self.font,self.fsize)
        self.render = self.font.render(self.text,True,self.color)

    def set_size(self,size):
        self.fsize = size
        self.font = pg.font.SysFont(self.font,self.fsize)
        self.render = self.font.render(self.text,True,self.color)

    def check_click(self,app):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            for widget in app.widgets:
                if isinstance(widget,TextBox):
                    widget.active = False
            self.active = True

    def get_text(self):
        return self.text
    
class Image(Widget):
    def __init__(self,image,pos):
        super().__init__()
        self.image = pg.image.load(image)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def set_image(self,image):
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def set_pos(self,pos):
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

class Button(Widget):
    def __init__(self,text,pos,color,bgColor,outlineColor,font,size,action):
        super().__init__()
        self.text = text
        self.pos = pos
        self.color = color
        self.bgColor = bgColor
        self.outlineColor = outlineColor
        self.font = font
        self.size = size
        self.action = action
        self.font = pg.font.SysFont(self.font,self.size)
        self.render = self.font.render(self.text,True,self.color)
        self.rect = self.render.get_rect().inflate(10,10)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.txt_rect = self.render.get_rect(center = self.rect.center)

    def draw(self,screen):
        pg.draw.rect(screen,self.bgColor,self.rect)
        pg.draw.rect(screen,self.outlineColor,self.rect.inflate(2,2),2)
        screen.blit(self.render,self.txt_rect)

    def set_text(self,text):
        self.text = text
        self.render = self.font.render(self.text,True,self.color)
        self.rect = self.render.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def set_pos(self,pos):
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def set_color(self,color):
        self.color = color
        self.render = self.font.render(self.text,True,self.color)

    def set_font(self,font):
        self.font = font
        self.font = pg.font.SysFont(self.font,self.size)
        self.render = self.font.render(self.text,True,self.color)

    def set_size(self,size):
        self.size = size
        self.font = pg.font.SysFont(self.font,self.size)
        self.render = self.font.render(self.text,True,self.color)

    def check_click(self,app):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.action:
                self.action()

class Label(Widget):
    def __init__(self,text,pos,color,font,size):
        super().__init__()
        self.text = text
        self.pos = pos
        self.color = color
        self.font = font
        self.size = size
        self.font = pg.font.SysFont(self.font,self.size)
        self.render = self.font.render(self.text,True,self.color)
        self.rect = self.render.get_rect(topleft = self.pos)


    def draw(self,screen):
        screen.blit(self.render,self.rect)

    def set_text(self,text):
        self.text = text
        self.render = self.font.render(self.text,True,self.color)
        self.rect = self.render.get_rect(topleft = self.pos)


    def set_pos(self,pos,wrt = 'topleft'):

        exec(f"self.rect.{wrt} = pos")
        self.pos = self.rect.topleft

    def set_color(self,color):
        self.color = color
        self.render = self.font.render(self.text,True,self.color)

    def set_font(self,font):
        self.font_name = font
        self.font = pg.font.SysFont(self.font_name,self.size)
        self.render = self.font.render(self.text,True,self.color)

    def set_size(self,size):
        self.size = size
        self.font = pg.font.SysFont(self.font_name,self.size)
        self.render = self.font.render(self.text,True,self.color)



class App:
    def __init__(self,x,y,name = "App"):
        self.screen = pg.display.set_mode((x,y))
        pg.display.set_caption(name)
        self.clock = pg.time.Clock()
        self.running = True
        self.fps = 60
        self.background_color = (255,255,255)
        self.widgets = []
        self.widget_count = 0
        
    def set_background_color(self,color):
        self.background_color = color

    def set_fps(self,fps):
        self.fps = fps
    
    def set_caption(self,name):
        pg.display.set_caption(name)

    def add_label(self,*,text,pos,color = (0,0,0),font = "Arial",size = 20):
        self.widgets.append(Label(text,pos,color,font,size))
        self.widgets[-1].id = self.widget_count
        self.widget_count += 1
        return self.widgets[-1]

    def add_button(self,*,text,pos,color = (0,0,0),bgColor = 'lightgray',outlineColor = 'grey',font = "Arial",size = 20,action = None):
        self.widgets.append(Button(text,pos,color,bgColor,outlineColor,font,size,action))
        self.widgets[-1].id = self.widget_count
        self.widget_count += 1
        return self.widgets[-1]

    def add_image(self,*,image,pos):
        self.widgets.append(Image(image,pos))
        self.widgets[-1].id = self.widget_count
        self.widget_count += 1
        return self.widgets[-1]

    def add_textbox(self,*,text,size,pos,color = 'black',activeColor = 'white',bgColor = 'lightgray',outlineColor = 'grey',font = "Arial",fsize = 20):
        self.widgets.append(TextBox(text,size,pos,color,activeColor,bgColor,outlineColor,font,fsize))
        self.widgets[-1].id = self.widget_count
        self.widget_count += 1
        return self.widgets[-1]
    
    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    for widget in self.widgets:
                        if isinstance(widget,Button) or isinstance(widget,TextBox):
                            widget.check_click(self)
                if event.type == pg.KEYDOWN:
                    for widget in self.widgets:
                        if isinstance(widget,TextBox):
                            if widget.active:
                                if event.key == pg.K_BACKSPACE:
                                    widget.set_text(widget.text[:-1])
                                elif event.key == pg.K_RETURN:
                                    widget.active = False
                                    print(widget.link)
                                    if widget.link != None:
                                        if isinstance(widget.link,TextBox): widget.link.active = True
                                        elif isinstance(widget.link,Button): widget.link.action()
                                        break
                                else:
                                    if widget.numbers_only:
                                        if event.unicode.isdigit():
                                            widget.set_text(widget.text + event.unicode)
                                    else:
                                        widget.set_text(widget.text + event.unicode)
            
            self.screen.fill(self.background_color)
            for widget in self.widgets:
                if not widget.hidden:
                    widget.draw(self.screen)
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    print("Xenon.py is not meant to be run as a standalone program. Please import it into your program.")
    sys.exit()