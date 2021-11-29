import random

from manim import *


class StarMotion(Scene):
    @staticmethod
    def func(pos):
        return np.array((random.randrange(-10, 10) / 10, 0, 0))

    def construct(self):
        stream_lines = StreamLines(self.func, stroke_width=2, max_anchors_per_line=30)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)


class RandomThingsMotion(Scene):
    @staticmethod
    def func(pos):
        return np.array((random.randrange(-10, 10) / 10, random.randrange(-10, 10) / 10, 0))

    def construct(self):
        stream_lines = StreamLines(self.func, stroke_width=2, max_anchors_per_line=300)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)


class SpawningAndFlowingAreaPicture(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[0]) * DOWN + np.cos(pos[1]) * LEFT + pos / 5
        stream_lines = StreamLines(
            func, x_range=[-3, 3, 0.2], y_range=[-2, 2, 0.2], padding=10,
            n_repeats=3,
            stroke_width=3,
            colors=[ORANGE, RED, DARK_BLUE]
        )

        spawning_area = Rectangle(width=6, height=4, stroke_width=.5)

        self.add(stream_lines, spawning_area)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)


class SpawningAndFlowingArea(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[0]) * UR + np.cos(pos[1]) * LEFT + pos / 5
        stream_lines = StreamLines(
            func,
            stroke_width=2,
            max_anchors_per_line=99999,
        )

        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)
