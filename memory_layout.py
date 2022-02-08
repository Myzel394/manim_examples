from manim import *


class RAMMemoryLayout(Scene):
    TEXT_PADDING = .5
    ARROW_PADDING = .1

    RAM_WIDTH = 3
    RAM_HEIGHT = 6

    # Kernel: 10%
    # Stack: 10%
    # Empty: 25%
    # Heap: 30%
    # BSS: 5%
    # Data: 10%
    # Text: 10%
    SEGMENT_PERCENTAGES = {
        "KERNEL": 0.1,
        "STACK": 0.1,
        "EMPTY": 0.25,
        "HEAP": 0.3,
        "BSS": 0.05,
        "DATA": 0.1,
        "TEXT": 0.1
    }
    SEGMENT_COLORS = {
        "KERNEL": RED_A,
        "STACK": BLUE_C,
        "EMPTY": BLACK,
        "HEAP": GOLD_C,
        "BSS": DARK_BLUE,
        "DATA": ORANGE,
        "TEXT": GRAY_C
    }

    def add_meta(self) -> None:
        title = Text("Memory-Layout").to_edge(UP)

        high_addresses_text = Text("0xFFFFFFFF", font_size=20)\
            .align_to(self.outer_rect, UP, LEFT)\
            .shift(LEFT * 3)
        low_addresses_text = Text("0x00000000", font_size=20)\
            .next_to(self.outer_rect, LEFT, buff=self.TEXT_PADDING)\
            .shift(DOWN * 2.9)
        high_addresses_arrow = Triangle()\
            .rotate(-PI * 0.5)\
            .set_fill(WHITE, 1)\
            .set_stroke(width=0)\
            .scale(.08)\
            .next_to(high_addresses_text, RIGHT, buff=self.ARROW_PADDING)
        low_addresses_arrow = Triangle()\
            .rotate(-PI * 0.5)\
            .set_fill(WHITE, 1)\
            .set_stroke(width=0)\
            .scale(.08)\
            .next_to(low_addresses_text, RIGHT, buff=self.ARROW_PADDING)

        self.add(
            title,
            self.outer_rect,
            high_addresses_text,
            high_addresses_arrow,
            low_addresses_text,
            low_addresses_arrow
        )

    def add_memory_segments(self) -> None:
        fake_rect = Rectangle(height=0).align_to(self.outer_rect, UP)
        align_mobject = fake_rect

        for name, percentage in self.SEGMENT_PERCENTAGES.items():
            color = self.SEGMENT_COLORS[name]
            rect = Rectangle(
                width=self.RAM_WIDTH,
                height=self.RAM_HEIGHT * percentage
            )\
                .set_fill(color, 1)\
                .set_stroke(width=0)\
                .next_to(align_mobject, DOWN, buff=0)
            align_mobject = rect
            self.add(rect)

        # Here's where I realized that Manim isn't meant to be used as an image creator,
        # but rather as a video engine. If I want to create awesome images, I should use
        # something like Figma. Using this, I could have created the image I'm creating here in a
        # minute...

    def construct(self):
        self.outer_rect = Rectangle(
            width=self.RAM_WIDTH,
            height=self.RAM_HEIGHT,
            color=WHITE
        )\
            .shift(DOWN * .5)

        self.add_memory_segments()
        self.add_meta()
