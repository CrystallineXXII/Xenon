import pygame as pg
import sys  


from classes import *




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