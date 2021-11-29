from typing import *

from manim import *
from manim_physics import *


class ElectricFieldExampleScene(Scene):
    old_field: ElectricField = None
    old_charges: Iterable[Charge]

    def create_field(self, *charges) -> ElectricField:
        return ElectricField(*charges)

    def transform_field(
            self,
            *charges: Charge,
            **kwargs
    ) -> None:
        new_field = self.create_field(*charges)

        if self.old_field:
            self.play(
                ReplacementTransform(
                    self.old_field,
                    new_field,
                    **kwargs
                ),
                *(
                    ReplacementTransform(
                        old_charge,
                        new_charge,
                        **kwargs
                    )
                    for old_charge, new_charge in zip(self.old_charges, charges)
                ),
            )
        else:
            self.play(
                *(
                    GrowFromCenter(charge)
                    for charge in charges
                )
            )
            self.play(FadeIn(new_field))
            self.wait()

        self.old_field = new_field
        self.old_charges = charges

    def get_intermediate_steps(
            self,
            start: np.ndarray,
            end: np.ndarray,
            *,
            accuracy: int = 10,
    ) -> Iterator[np.ndarray]:
        accuracy += 2
        diff = end - start
        value_per_part = diff / accuracy

        for multiplier in range(1, accuracy + 1):
            yield start + (value_per_part * multiplier)

    def transform_field_seamlessly(
            self,
            *charges: Charge,
            accuracy: int = 10,
            run_time: int = 2
    ) -> None:
        """Transforms an electric field smoothly without big a big gap between two charges
        moving.

        Can not be used for initial rendering.
        """
        run_time_per_step = run_time / accuracy

        intermediate_steps_per_charge = (
            self.get_intermediate_steps(
                old_charge.get_center(),
                new_charge.get_center(),
                accuracy=accuracy
            )
            for old_charge, new_charge in zip(self.old_charges, charges)
        )
        charges_per_step = (
            [
                Charge(charge_data.magnitude, position)
                for charge_data, position in zip(charges, charge_positions)
            ]
            for charge_positions in zip(*intermediate_steps_per_charge)
        )

        for charges in charges_per_step:
            self.transform_field(
                *charges,
                run_time=run_time_per_step,
                rate_func=rate_functions.linear
            )

    def construct(self):
        self.transform_field(
            Charge(-1, LEFT * 2),
            Charge(1, RIGHT)
        )

        self.transform_field_seamlessly(
            Charge(-1, LEFT * 2 + UP * 2),
            Charge(1, RIGHT),
        )
        self.wait()


class BarMagnetExample(Scene):
    def construct(self):
        bar1 = BarMagnet().rotate(PI / 2).shift(LEFT * 3.5)
        bar2 = BarMagnet().rotate(PI / 2 * -1).shift(RIGHT * 3.5)

        bar1.set_opacity(.3)
        bar2.set_opacity(.3)
        bar1.set_stroke(BLACK, width=0)
        bar2.set_stroke(BLACK, width=0)

        self.add(BarMagneticField(bar1, bar2, colors=[GRAY, RED_D, YELLOW, GREEN, BLUE]))
        self.add(bar1, bar2)


class BarMagnetRotatingExample(Scene):
    ROTATION_DURATION = .05

    def construct(self):
        old_bar = None
        old_rect = None
        old_field = None
        padding = .05
        temp_bar = BarMagnet()
        width = temp_bar.width + padding
        height = temp_bar.height + padding

        for rotation_percentage in range(0, 101, 2):
            rotation_amount = 2 * PI * rotation_percentage / 100 * -1

            bar = BarMagnet().rotate(rotation_amount)
            rect = Rectangle(
                width=width,
                height=height,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=0,
            )\
                .scale(1.2)\
                .next_to(bar, ORIGIN)\
                .rotate(rotation_amount)
            field = BarMagneticField(bar)

            if old_bar:
                self.play(
                    ReplacementTransform(
                        old_field,
                        field,
                        run_time=self.ROTATION_DURATION,
                        rate_func=rate_functions.linear
                    ),
                    ReplacementTransform(
                        old_rect,
                        rect,
                        run_time=self.ROTATION_DURATION,
                        rate_func=rate_functions.linear
                    ),
                    ReplacementTransform(
                        old_bar,
                        bar,
                        run_time=self.ROTATION_DURATION,
                        rate_func=rate_functions.linear
                    ),
                )
            else:
                self.add(field)
                self.add(rect)
                self.add(bar)

            old_field = field
            old_rect = rect
            old_bar = bar


class CreateElectricFieldScene(Scene):
    def construct(self):
        charge1 = Charge(-1, LEFT * 2)
        charge2 = Charge(1, RIGHT * 2)
        none_field = ElectricField(Charge(-1, UP * 5e10))
        field = ElectricField(charge1, charge2)

        self.play(
            FadeIn(none_field)
        )
        self.wait()
        # Show charge1 and charge2 simultaneously, delay the field change by 0.2 seconds
        self.play(
            AnimationGroup(
                AnimationGroup(
                    GrowFromCenter(charge1),
                    GrowFromCenter(charge2),
                ),
                ReplacementTransform(none_field, field),
                lag_ratio=.2
            )
        )
        self.wait()


class MultiPendulumScene(SpaceScene):
    """Shows the trace of a pendulum without it's bobs."""

    def construct(self):
        p = MultiPendulum(
            LEFT * .5, LEFT, LEFT * 2,
        )

        self.add(p)
        self.make_rigid_body(p.bobs)
        p.start_swinging()
        self.add(
            TracedPath(
                p.bobs[-1].get_center,
                stroke_color=BLUE,
            )
        )
        self.wait(40)


class FallingEquation(SpaceScene):
    def construct(self):
        equation = MathTex(
            "{{U}} {{_{i}}{{n}}{{d}}} }} {{=}} {{-}}{{n}} "
            "{{\cdot}} {{B}} {{\cdot}} {{v}} {{\cdot}} {{l}} _{{{e}}{{f}}{{f}}} }}",
        )\
            .shift(UP)
        ground = Line([-4, -1.5, 0], [4, -1.5, 0])

        self.add(equation, ground)
        self.make_rigid_body(*equation.submobjects)
        self.make_static_body(
            ground,
            # Ensures that characters don't fall through the ground
            ground.copy().shift(DOWN * 0.01),
            ground.copy().shift(DOWN * 0.03),
            ground.copy().shift(DOWN * 0.05),
            ground.copy().shift(DOWN * 0.07)
        )
        self.wait(10)
