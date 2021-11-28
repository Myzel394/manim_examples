import math

from manim import *
from manim_physics import *

IS_DEBUG = False
FULL_CIRCLE = PI * 2

# 1% rotation per step
ROTATION_AMOUNT_PER_STEP = FULL_CIRCLE * 0.01
ROTATION_DURATION = 0.02

if IS_DEBUG:
    ROTATION_AMOUNT_PER_STEP = FULL_CIRCLE * 0.05


class RotatingBarMagnet(BarMagnet):
    def __init__(self, rotation: float = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rotate(rotation)

    def step(self):
        self.rotate(ROTATION_AMOUNT_PER_STEP)
        return self

    def get_required_steps_amount(self) -> int:
        return math.ceil(PI * 2 / ROTATION_AMOUNT_PER_STEP)


class MultipleMagnetsRotatingScene(Scene):
    """A magnetic field with multiple bar magnets rotating."""

    def construct(self):
        old_magnets = [
            RotatingBarMagnet().shift(LEFT * 2),
            RotatingBarMagnet().shift(RIGHT * 2).rotate(FULL_CIRCLE / 2),

            RotatingBarMagnet().to_corner(UP + RIGHT, buff=.2).rotate(FULL_CIRCLE / 4).scale(.3),
            RotatingBarMagnet().to_corner(DOWN + RIGHT, buff=.2).scale(.3),
            RotatingBarMagnet().to_corner(UP + LEFT, buff=.2).scale(.3),
            RotatingBarMagnet().to_corner(DOWN + LEFT, buff=.2).rotate(FULL_CIRCLE / 4).scale(.3),
        ]
        old_field = BarMagneticField(*old_magnets)

        self.add(old_field)
        self.add(*old_magnets)

        for _ in range(old_magnets[0].get_required_steps_amount()):
            new_magnets = [
                magnet.step().copy()
                for magnet in old_magnets
            ]
            field = BarMagneticField(*new_magnets)

            self.play(
                ReplacementTransform(
                    old_field,
                    field,
                    run_time=ROTATION_DURATION,
                    rate_func=rate_functions.linear
                ),
                *(
                    ReplacementTransform(
                        old_magnet,
                        new_magnet,
                        run_time=ROTATION_DURATION,
                        rate_func=rate_functions.linear
                    )
                    for old_magnet, new_magnet in zip(old_magnets, new_magnets)
                )
            )

            old_magnets = new_magnets
            old_field = field

