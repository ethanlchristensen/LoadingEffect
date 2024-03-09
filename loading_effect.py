import time
import string
import random
import bruhcolor
from bruhanimate.bruhffer import Buffer
from bruhanimate.bruhscreen import Screen
from bruhanimate.bruheffects import SnowEffect


class A:
    def __init__(self, x, y, length, char_halt = 1, color_halt = 1, gradient_length = 1):
        self.x = x
        self.y = y
        self.__gradient = [c for c in [232, 232,232, 232, 233, 233, 233, 233,234, 234, 234, 234,235, 235,235, 235, 236, 236,236, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255] for _ in range(gradient_length)]
        self.__char_halt = char_halt
        self.__char_frame_number = 0
        self.__color_halt = color_halt
        self.__color_frame_number = 0
        self.length = length
        self.string_chars = [None for _ in range(self.length)]
        self.string_colors = [self.__gradient[i % len(self.__gradient)] for i in range(self.length)]
        self.colored_chars = [bruhcolor.bruhcolored(c, color=color) for c, color in zip(self.string_chars, self.string_colors)]
        
    def generate(self, frame_number: int):
        if frame_number % self.__char_halt == 0:
            self.__char_frame_number += 1
            for i, c in enumerate(self.string_chars):
                if not c: self.string_chars[i] = random.choice(string.ascii_letters + "1234567890!@#$%^&*()_+-=<>,.:\";'{}[]?/")
                elif random.random() < 0.6: self.string_chars[i] = random.choice(string.ascii_letters + "1234567890!@#$%^&*()_+-=<>,.:\";'{}[]?/")
        if frame_number % self.__color_halt == 0:
            self.__color_frame_number += 1
            self.string_colors = [self.__gradient[(i - self.__color_frame_number) % len(self.__gradient)] for i in range(self.length)]
        
        self.colored_chars = [bruhcolor.bruhcolored(c, color=color) for c, color in zip(self.string_chars, self.string_colors)]


class Bubble:
    def __init__(self, bubbles=5):
        self.bubbles = bubbles
        self.bubble_chars = ["." for _ in range(self.bubbles)]
        self.pos = 0
        self.inc_val = 1
    
    def update(self):
        self.bubble_chars[self.pos] = "•"
        self.bubble_chars[self.pos - self.inc_val] = "."
        if self.pos >= self.bubbles - 1:
            self.inc_val = -1
        elif self.pos <= 0:
            self.inc_val = 1
        self.pos += self.inc_val


class GenerateBubble:
    def __init__(self, x, y, bubbles = 4, halt = 1):
        self.x = x
        self.y = y
        self.__halt = halt
        self.__main_text = list("Generating")
        self.__bubble_generator = Bubble(bubbles)
        self.chars = self.__main_text + self.__bubble_generator.bubble_chars
    
    def generate(self, frame_number: int):
        if frame_number % self.__halt == 0:
            self.__bubble_generator.update()
            self.chars = self.__main_text + self.__bubble_generator.bubble_chars
    
  
class Cradle:
    def __init__(self, cradle_length=5):
        self.cradle_length = cradle_length
        self.cradle_chars = ["." for _ in range(self.cradle_length)]
        self.ball = "•"
        self.ball_pos = -1

    def update(self):
        self.cradle_chars[0] = self.ball
        self.ball_pos = 0
    
    def push_ball(self) -> bool:
        self.cradle_chars[self.ball_pos] = "."
        if self.ball_pos == self.cradle_length - 1:
            self.ball_pos = -1
            return True
        else:
            self.ball_pos = (self.ball_pos + 1) % self.cradle_length
            self.cradle_chars[self.ball_pos] = self.ball
            return False

  
class GenerateCradle:
    def __init__(self, x, y, cradle_length = 4, halt = 1):
        self.x = x
        self.y = y
        self.__halt = halt
        self.__main_text = list("Generating")
        self.__gradle_generator = Cradle(cradle_length)
        self.chars = self.__main_text + self.__gradle_generator.cradle_chars
        self.free = True
    
    def generate(self, frame_number: int):
        if self.free:
            self.__gradle_generator.update()
            self.free = False
        else:
            if frame_number % self.__halt == 0:
                self.free = self.__gradle_generator.push_ball()
            
        self.chars = self.__main_text + self.__gradle_generator.cradle_chars
                

def main(screen: Screen) -> None:

    a = A(0, 1, 30, 1, 1, 5)
    g = GenerateCradle(a.x + a.length + 1, 1, 5, 6)
    
    back_buffer = Buffer(screen.height, screen.width)
    front_buffer = Buffer(screen.height, screen.width)
    effect = SnowEffect(Buffer(screen.height, screen.width), " ")
    effect.smart_transparent = False
    effect.collision = True
    
    effect_halt = 5
    
    frame = 0
    
    try:
        while True:
            
            if frame % effect_halt == 0:
                effect.render_frame(frame)
            
            a.generate(frame)
            if a.string_colors[-1] == 255 or not g.free:
                g.generate(frame)

            back_buffer.sync_with(effect.buffer)
            
            for i, c in enumerate(a.colored_chars):
                back_buffer.put_char(a.x + i, a.y, c.colored)
            for i, c in enumerate(g.chars):
                back_buffer.put_char(g.x + i, g.y, c)
                
            for y, x, val in front_buffer.get_buffer_changes(back_buffer):
                screen.print_at(val, x, y, 1)
                
            front_buffer.sync_with(back_buffer)
            
            time.sleep(0.01)
            
            frame += 1
            
    except KeyboardInterrupt:
        pass    
    

if __name__ == "__main__":
    Screen.show(main)