from manim import *
import numpy as np


class ExplanationScene(Scene):
    def construct(self):
        es = VGroup(
            Circle(opacity=0, stroke_color=RED),
            Text("Es", color=RED).scale(.6),
        ).shift(UP * 2.8)
        ich = VGroup(
            RoundedRectangle(opacity=0, stroke_color=BLUE, width=2, height=1, corner_radius=.2),
            Text("Ich", color=BLUE)
        )
        ueber = VGroup(
            Circle(opacity=0, stroke_color=WHITE),
            Text("Über-Ich", color=WHITE).scale(.6)
        ).shift(DOWN * 2.8)

        all = VGroup(
            es,
            ich,
            ueber,
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ShowCreation(es[0], run_time=2),
                    Write(es[1], run_time=2),
                ),
                AnimationGroup(
                    ShowCreation(ich[0], run_time=2),
                    Write(ich[1], run_time=2),
                ),
                AnimationGroup(
                    ShowCreation(ueber[0], run_time=2),
                    Write(ueber[1], run_time=2),
                ),
                lag_ratio=.4
            )
        )

        self.play(
            ApplyMethod(all.shift, LEFT * 2.5)
        )

        # Es und Triebe Dots animation

        es_trieb_circle_1 = Annulus(inner_radius=0, outer_radius=.6, color=RED)
        es_trieb_circle_2 = Annulus(inner_radius=.55, outer_radius=.6, color=RED)
        es_trieb_circle_3 = es_trieb_circle_1.copy()
        es_trieb_text = Text("Trieb", color=RED).scale(.4)

        es_trieb = VGroup(
            es_trieb_circle_1,
            es_trieb_circle_2,
            es_trieb_circle_3,
            es_trieb_text,
        ).shift(UP * 2.8 + RIGHT * .5)

        es_trieb.z_index = 0

        self.play(GrowFromCenter(es_trieb_circle_1))
        self.add(es_trieb_text)
        self.play(
            ReplacementTransform(es_trieb_circle_1, es_trieb_circle_2),
        )

        uber_circle_1 = Annulus(inner_radius=0, outer_radius=.6, color=WHITE)
        uber_circle_2 = Annulus(inner_radius=.55, outer_radius=.6, color=WHITE)
        uber_circle_3 = uber_circle_1.copy()
        uber_text = Text("Wert", color=WHITE).scale(.4)

        uber_group = VGroup(
            uber_circle_1,
            uber_circle_2,
            uber_circle_3,
            uber_text,
        ).shift(DOWN * 2.8 + RIGHT * .5)

        uber_group.z_index = 0

        self.play(GrowFromCenter(uber_circle_1))
        self.add(uber_text)
        self.play(
            ReplacementTransform(uber_circle_1, uber_circle_2),
        )

        # Clash dots
        es_line = Line(es_trieb_circle_2.get_corner(DOWN), RIGHT * .5, color=RED)
        es_line_2 = Line(es_line.start, es_line.end + UP * .6, color=RED)
        es_line_3 = Line(es_line_2.end, es_line_2.end, color=RED)
        uber_line = Line(uber_circle_2.get_corner(UP), RIGHT * .5, color=WHITE)
        uber_line_2 = Line(uber_line.start, uber_line.end + DOWN * .6, color=WHITE)
        uber_line_3 = Line(uber_line_2.end, uber_line_2.end, color=WHITE)

        self.play(
            AnimationGroup(
                ShowCreation(es_line, run_time=2, rate_func=rush_into),
                ShowCreation(uber_line, run_time=2, rate_func=rush_into)
            )
        )
        self.play(
            AnimationGroup(
                ReplacementTransform(es_line, es_line_2, run_time=.4, rate_func=slow_into),
                ReplacementTransform(uber_line, uber_line_2, run_time=.4, rate_func=slow_into)
            )
        )

        vermittlung_black = Circle(radius=.6, fill_opacity=1, fill_color=BLACK, stroke_width=0)
        vermittlung_1 = Annulus(
            inner_radius=0,
            outer_radius=.6,
            color=BLUE,
        )
        vermittlung_2 = Annulus(inner_radius=.55, outer_radius=.6, color=BLUE)
        vermittlung_text = Text("Vermittlung", color=BLUE).scale(.2)

        ver = VGroup(
            vermittlung_black,
            vermittlung_1,
            vermittlung_2,
            vermittlung_text,
        ).shift(RIGHT * .5)

        ver.z_index = 2

        self.play(
            GrowFromCenter(vermittlung_black),
            GrowFromCenter(vermittlung_1),
        )
        self.add(vermittlung_text)
        self.play(
            ReplacementTransform(vermittlung_1, vermittlung_2),
        )

        # Scale dots
        self.play(
            AnimationGroup(
                ReplacementTransform(es_trieb_circle_2, es_trieb_circle_3),
                ReplacementTransform(uber_circle_2, uber_circle_3),
            )
        )
        self.remove(es_trieb_text, uber_text)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(
                        AnimationGroup(
                            ApplyMethod(es_trieb_circle_3.shift, DOWN * 2.8),
                            ReplacementTransform(es_line_2, es_line_3),
                        ),
                        AnimationGroup(
                            ApplyMethod(uber_circle_3.shift, UP * 2.8),
                            ReplacementTransform(uber_line_2, uber_line_3),
                        ),
                        ScaleInPlace(vermittlung_black, 1),
                    ),
                    AnimationGroup(
                        FadeToColor(vermittlung_text, color=PURPLE_C),
                        FadeToColor(vermittlung_2, color=PURPLE_C),
                    ),
                    lag_ratio=.3
                ),
            )
        )




