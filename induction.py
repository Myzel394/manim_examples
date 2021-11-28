from manim import *
from manim_physics import *

DEFAULT_PADDING = .3
DEFAULT_BAR_SIZE = 1


class HorseShoeMagnet(VGroup):
    def __init__(
        self,
        width: float = 6,
        height: float = 6,
        bar_width: float = DEFAULT_PADDING,
        bar_height: float = DEFAULT_PADDING,
        field_x_padding: float = DEFAULT_PADDING,
        field_y_padding: float = DEFAULT_PADDING,
        field_density: float = 2,
        magnets: list[BarMagnet] = None,
        create_bar: bool = True,
        **kwargs
    ):
        magnets = magnets or []

        field_width = width - bar_width
        field_height = height - (bar_height * 2)

        bar_magnets = [*magnets]
        surrounding_rectangle = Rectangle(width=0, height=height)

        # Ensures that there is a field
        self.bar_magnet = BarMagnet(width=width, height=height * 5)

        if create_bar:
            bar_magnets.insert(0, self.bar_magnet)

        self.field = BarMagneticField(
            *bar_magnets,
            x_range=[
                -(field_width / 2),
                (field_width / 2 - field_x_padding),
                1 / field_density
            ],
            y_range=[
                -(field_height / 2 - field_y_padding),
                (field_height / 2 - field_y_padding),
                1 / field_density
            ]
        )

        self.north_rectangle = Rectangle(
            width=field_width,
            height=bar_height,
            fill_opacity=1,
            color=RED,
            stroke_width=0,
        )\
            .align_to(surrounding_rectangle, DOWN)
        self.north_side_wall = Rectangle(
            width=bar_width,
            height=height / 2,
            fill_opacity=1,
            color=RED,
            stroke_width=0,
        )\
            .align_to(self.north_rectangle, RIGHT + DOWN)\
            .shift(RIGHT)
        self.north_label = Tex("N").next_to(self.north_rectangle, ORIGIN)
        self.north_parts = VGroup(
            self.north_rectangle,
            self.north_side_wall,
        )

        self.south_rectangle = Rectangle(
            width=field_width,
            height=bar_height,
            fill_opacity=1,
            color=BLUE,
            stroke_width=0,
        )\
            .align_to(surrounding_rectangle, UP)
        self.south_side_wall = Rectangle(
            width=bar_width,
            height=height / 2,
            fill_opacity=1,
            color=BLUE,
            stroke_width=0,
        )\
            .align_to(self.south_rectangle, RIGHT + UP)\
            .shift(RIGHT)
        self.south_label = Tex("S").next_to(self.south_rectangle, ORIGIN)
        self.south_parts = VGroup(
            self.south_rectangle,
            self.south_side_wall,
        )

        super().__init__(**kwargs)
        self.add(
            self.field,
            VGroup(
                self.north_parts,
                self.south_parts,
            ),
            self.north_label,
            self.south_label
        )
        self.add(*magnets, self.bar_magnet.set_opacity(.2))


class FirstFormulaExplainedScene(Scene):
    def construct(self):
        magnet = HorseShoeMagnet(field_density=8, magnets=[BarMagnet().scale(.1)])

        self.add(magnet)
