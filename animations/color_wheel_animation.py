from animations.animation import Animation, LoopMode
from colors.color import HSV
from auxiliary.config import Config

from controllers.led_controller import LedController


class ColorWheelAnimation(Animation):

    name = "Color Wheel"

    def __init__(self, led_controller: LedController, config: Config):
        super().__init__(led_controller, config)
        self.loop_mode = LoopMode[config.get('loop_mode', 'ENDLESS')]
        self.scale_factor = config.get('scale_factor', 1.0)
        self.duration = config.get('duration', 20.0)
        self.target_frame_rate = config.get('target_frame_rate', 40.0)

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_update(self):
        t = self.anim_progress

        for i in range(self.led_controller.usable_led_count):
            b = self.scale_factor / self.led_controller.usable_led_count
            self.led_controller.set_single_color(i, HSV(t + (b * i), 1, 1).rgb_255())

        self.led_controller.show()
