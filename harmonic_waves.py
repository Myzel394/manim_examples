from manim import *

DOTS_AMOUNT = 20
RANGE = (-6, 6)


class MultiplePointsOnOneImaginaryLine(Scene):
    def construct(self):
        size = max(*RANGE) - min(*RANGE)
        distance = size / DOTS_AMOUNT

        for multiplier in range(DOTS_AMOUNT):
            position_x = RANGE[0] + distance * multiplier
            position = (position_x, 0, 0)
            dot = Dot(position)

            self.add(dot)


class TwoSinusFunctionsOneDelayed(Scene):
    def construct(self):
        axes = Axes(
            x_range=[*RANGE],
            y_range=[-2, 2, 1],
            x_length=10,
            x_axis_config={
                "numbers_to_include": np.arange(-10, 10, 2),
                "numbers_with_elongated_ticks": np.arange(-10, 10, 2),
            },
            tips=False,
        )

        axes_labels = axes.get_axis_labels(
            y_label="",
            x_label="\\text{t in s}"
        )
        first_graph = axes.plot(lambda x: np.sin(x * 2), color=WHITE)
        first_label = axes.get_graph_label(
            first_graph,
            "\\text{Erster Oszillator}",
            x_val=-1.6 * PI,
            direction=UP * 3,
        )
        second_graph = axes.plot(lambda x: np.sin(x * 2 - 4), color=RED)
        second_label = axes.get_graph_label(
            first_graph,
            "\\text{Zweiter Oszillator}",
            x_val=1.6 * PI,
            direction=DOWN * 3,
            color=RED
        )

        self.add(axes_labels, first_graph, second_graph, first_label, second_label)


class TwoSinusFunctionsOneDelayedButOnlyDots(Scene):
    INVISIBLE_GRAPH_OPACITY = 0.05

    def construct(self):
        axes = Axes(
            x_range=[*RANGE],
            y_range=[-2, 2, 1],
            x_length=10,
            x_axis_config={
                "numbers_to_include": np.arange(-10, 10, 2),
                "numbers_with_elongated_ticks": np.arange(-10, 10, 2),
            },
            tips=False,
        )

        axes_labels = axes.get_axis_labels(
            y_label="",
            x_label="\\text{t in s}"
        )
        first_graph = axes.plot(
            lambda x: np.sin(x * 2),
            color=WHITE,
            stroke_opacity=self.INVISIBLE_GRAPH_OPACITY
        )
        first_graph.set_stroke_opacity(self.INVISIBLE_GRAPH_OPACITY)
        first_label = axes.get_graph_label(
            first_graph,
            "\\text{Erster Oszillator}",
            x_val=-1.6 * PI,
            direction=UP * 3,
        )
        second_graph = axes.plot(
            lambda x: np.sin(x * 2 - 4),
            color=RED,
            stroke_opacity=self.INVISIBLE_GRAPH_OPACITY
        )
        second_label = axes.get_graph_label(
            first_graph,
            "\\text{Zweiter Oszillator}",
            x_val=1.6 * PI,
            direction=DOWN * 3,
            color=RED
        )
        size = max(*RANGE) - min(*RANGE)
        distance = size / DOTS_AMOUNT

        self.add(axes_labels, first_graph, second_graph, first_label, second_label)

        for multiplier in range(DOTS_AMOUNT):
            position_x = RANGE[0] + distance * multiplier
            point = axes.i2gp(position_x, first_graph)
            dot = Dot(point)

            self.add(dot)

        for multiplier in range(DOTS_AMOUNT):
            position_x = RANGE[0] + distance * multiplier
            point = axes.i2gp(position_x, second_graph)
            dot = Dot(point, color=RED)

            self.add(dot)

