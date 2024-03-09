import time
import string
import random
import bruhcolor
from bruhanimate.bruhffer import Buffer
from bruhanimate.bruhscreen import Screen
from bruhanimate.bruheffects import SnowEffect


class GradientNoise:
    def __init__(self, x, y, length, char_halt=1, color_halt=1, gradient_length=1):
        self.x = x
        self.y = y
        self.__gradient_length = gradient_length
        # colors to use for gradient
        self.__gradient = [c for c in [232,232,232,232,233,233,233,233,234,234,234,234,235,235,235,235,236,236,236,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255] for _ in range(self.__gradient_length)]
        # delay to changing the chars in the noise
        self.__char_halt = char_halt
        self.__char_frame_number = 0
        # delay to change the gradient shift
        self.__color_halt = color_halt
        self.__color_frame_number = 0
        self.length = length
        
        self.string_chars = [None for _ in range(self.length)]
        self.string_colors = [self.__gradient[i % len(self.__gradient)] for i in range(self.length)]
        self.colored_chars = [bruhcolor.bruhcolored(c, color=color) for c, color in zip(self.string_chars, self.string_colors)]

    # change the gradient
    def update_gradient(self, gradient):
        self.__gradient = [c for c in gradient for _ in range(self.__gradient_length)]


    def generate(self, frame_number: int):
        # is it time to change the noise chars?
        if frame_number % self.__char_halt == 0:
            self.__char_frame_number += 1
            for i, c in enumerate(self.string_chars):
                # frame == 0 basically
                if not c:
                    self.string_chars[i] = random.choice(
                        string.ascii_letters + "1234567890!@#$%^&*()_+-=<>,.:\";'{}[]?/"
                    )
                # randomly decide to update this char to a new one
                elif random.random() < 0.6:
                    self.string_chars[i] = random.choice(
                        string.ascii_letters + "1234567890!@#$%^&*()_+-=<>,.:\";'{}[]?/"
                    )
        # is it time to change the gradient position?
        if frame_number % self.__color_halt == 0:
            self.__color_frame_number += 1
            self.string_colors = [
                self.__gradient[(i - self.__color_frame_number) % len(self.__gradient)]
                for i in range(self.length)
            ]

        # update the color characters exposed to the main program
        self.colored_chars = [
            bruhcolor.bruhcolored(c, color=color)
            for c, color in zip(self.string_chars, self.string_colors)
        ]


class Bubble:
    def __init__(self, bubbles=5):
        self.bubbles = bubbles
        self.bubble_chars = ["." for _ in range(self.bubbles)]
        self.pos = 0
        self.inc_val = 1

    def update(self):
        # for each update call, push the bubble back
        # and forth
        self.bubble_chars[self.pos] = "•"
        self.bubble_chars[self.pos - self.inc_val] = "."
        if self.pos >= self.bubbles - 1:
            self.inc_val = -1
        elif self.pos <= 0:
            self.inc_val = 1
        self.pos += self.inc_val


class GenerateBubble:
    """
    Creates the "Generating" text and the bubble that
    moves back and forth
    """
    def __init__(self, x, y, bubbles=4, halt=1):
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
    """
    Class to handle sending bubble from beggining
    to end only.
    """
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
    """
    Class to handle the "Generating" text and updating
    the cradle ball to get sent to the end.
    """
    def __init__(self, x, y, cradle_length=4, halt=1):
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
    # place the gradient noise
    noise_1 = GradientNoise(x=0, y=1, length=30, char_halt=20, color_halt=1, gradient_length=5)
    noise_2 = GradientNoise(x=0, y=3, length=30, char_halt=1, color_halt=20, gradient_length=5)
    noise_2.update_gradient([21, 57, 93, 129, 165, 201, 165, 129, 93, 57])
    # place the generate text next to the noise
    generate_1 = GenerateCradle(x=noise_1.x + noise_1.length + 1, y=1, cradle_length=5, halt=6)
    generate_2 = GenerateBubble(x=noise_2.x + noise_2.length + 1, y=3, bubbles=5, halt=20)
    
    

    back_buffer = Buffer(height=screen.height, width=screen.width)
    front_buffer = Buffer(height=screen.height, width=screen.width)
    effect = SnowEffect(Buffer(height=screen.height, width=screen.width), " ")
    
    # have to add these two lines. normally this is handled
    # by a bruhanimate.bruhrenderer
    effect.smart_transparent = False
    effect.collision = True

    # delay to generate the next effect frame
    effect_halt = 5

    # track the elapsed frames
    current_frame = 0

    try:
        while True:
            # is it time to generate the next effect frame?
            if current_frame % effect_halt == 0:
                effect.render_frame(current_frame)
                back_buffer.sync_with(effect.buffer)

            # update the gradient noise
            noise_1.generate(current_frame)
            noise_2.generate(current_frame)
            
            # in this case we check if the white color has reached 
            # the end of the noise, thus triggering a bubble to 
            # propogate down, generate.free tells us if we need to keep
            # calling generate on the generate dots
            if noise_1.string_colors[-1] == 255 or not generate_1.free:
                generate_1.generate(current_frame)
            generate_2.generate(current_frame)
        
            # add the updates to the back buffer
            for i, c in enumerate(noise_1.colored_chars):
                back_buffer.put_char(noise_1.x + i, noise_1.y, c.colored)
            for i, c in enumerate(noise_2.colored_chars):
                back_buffer.put_char(noise_2.x + i, noise_2.y, c.colored)
            
            # add the updates to the back buffer  
            for i, c in enumerate(generate_1.chars):
                back_buffer.put_char(generate_1.x + i, generate_1.y, c)
            for i, c in enumerate(generate_2.chars):
                back_buffer.put_char(generate_2.x + i, generate_2.y, c)

            # push the changes to the screen
            for y, x, val in front_buffer.get_buffer_changes(back_buffer):
                screen.print_at(val, x, y, 1)

            # sync the back and front
            front_buffer.sync_with(back_buffer)

            time.sleep(0.01)
            current_frame += 1
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    Screen.show(main)
