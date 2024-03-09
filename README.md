# LoadingEffect

A simple effect using my [bruhanimate](https://github.com/FNBBDevs/bruhanimate) library. Here I wanted to create a simple loading / generating / progress animation that involved some noise / gradients.

# Installation

Make sure you have Python 3.8 or higher installed. You can install the bruhanimate package using either pip or poetry:

## Using pip (from requirements.txt)
```bash
pip install -r requirements.txt
```

## Using poetry (from pyproject.toml)
```bash
poetry install
```

# Usage

The main classes to use are `GradientNoise` and one of `GenerateBubble` or `GenerateCradle`.

This isn't an effect in bruhanimate, so the buffers, and effect pieces need to be set up.

The main concept to understand is how bruhanimate works. We use the `Screen` class, and create a function we will pass into the `Screen.show()` command.

```python

from bruhanimate.bruhscreen import Screen

def main(screen: Screen):
    # place some text
    screen.print_center("Hello World!", y=screen.height // 2, width=len("Hello World!"))
    # catch the end of the program
    input()
    # you should now have "Hello World" in the center of your termnial

if __name__ == "__main__":
    Screen.show(main)

```

In the main function we create the buffers we need and update them as we need. The `GradientNoise`, `GenerateBubble`, or `GenerateCradle` have `generate()` functions that update the state of the items we want to put in the buffer.

```python

import time
import string
import random
import bruhcolor
from bruhanimate.bruhffer import Buffer
from bruhanimate.bruhscreen import Screen

class GradientNoise: . . . # as it is in loading_effect.py
class GenerateBubble: . . . # as it is in loading_effect.py

def main(screen):
    noise = GradientNoise(x=0, y=0, length=30, char_halt=1, color_halt=20, gradient_length=5)
    noise.update_gradient([21, 57, 93, 129, 165, 201, 165, 129, 93, 57])
    generate = GenerateBubble(x=noise.x + noise.length + 1, y=0, bubbles=5, halt=20)

    back_buffer = Buffer(height=screen.height, width=screen.width)
    front_buffer = Buffer(height=screen.height, width=screen.width)

    current_frame = 0
    while True:
        try:
            # update the noise state
            noise.generate(current_frame)
            # update the "Generating....." state
            generate.generate(current_frame)

            # apply the changes to the buffer
            for i, c in enumerate(noise.colored_chars):
                back_buffer.put_char(noise.x + i, noise.y, c.colored)

            # apply the changes to the buffer
            for i, c in enumerate(generate.chars):
                back_buffer.put_char(generate.x + i, generate.y, c)

            # push the changes to the terminal
            for y, x, val in front_buffer.get_buffer_changes(back_buffer):
                screen.print_at(val, x, y, 1)

            front_buffer.sync_with(back_buffer)

            time.sleep(0.01)
            current_frame += 1
        except KeyboardInterrupt:
            back_buffer.clear_buffer()
            back_buffer.put_at_center(y=screen.height // 2, text="Press [Enter] to exit")
            for y, x, val in front_buffer.get_buffer_changes(back_buffer):
                screen.print_at(val, x, y, 1)
            input()
            return
        

if __name__ == "__main__":
    Screen.show(main)

```