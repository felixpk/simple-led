import time

from animations import helper
from animations.animation import Animation
from noise import pnoise1

from colors.color import RGB255


class FireAnimation(Animation):
    def on_start(self):
        self.led_controller.clear()
        self.led_controller.show()

    def on_stop(self):
        pass

    def on_update(self):
        t = self.anim_progress
        print(time.time_ns() * 0.0000000000000000000001)
        noise = (pnoise1(time.time(), 4, 0.5) + 1) * 0.5
        # print(noise)

        start_color = RGB255(255, 0, 0)
        # end_color = helper.interpolate_color(noise, RGB255(255, 255, 0), RGB255(50, 50, 0))

        # colors = helper.color_gradient(start_color, end_color, 90)

        # self.led_controller.set_colors(colors)
        # self.led_controller.show()
