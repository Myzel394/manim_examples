from pprint import pprint
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

        self.add(BarMagneticField(bar1, bar2))
        self.add(bar1, bar2)
