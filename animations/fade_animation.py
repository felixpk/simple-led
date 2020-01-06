from animations import helper
from animations.animation import Animation, LoopMode
from helper.config import Config
from colors import color
from colors.color import RGB255
from controllers.led_controller import LedController
from helper.log_manager import LogManager

LOGMAN = LogManager(__name__)


class FadeAnimation(Animation):

    name = 'Fade'

    customizable_properties = {
        "Duration": int,
    }

    def __init__(self, led_controller: LedController, **kwargs):
        super().__init__(led_controller)

        self.loop_mode = LoopMode[kwargs.get('loop_mode', 'ENDLESS')]
        self.duration = kwargs.get('duration', 5.0)
        self.target_frame_rate = kwargs.get('target_frame_rate', 10.0)

        self.start_color: RGB255 = color.random_rgb_255()
        self.end_color: RGB255 = color.random_rgb_255()

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_update(self):
        t = self.anim_progress

        current_color = helper.lerp_color_255(t,
                                              self.start_color,
                                              self.end_color)

        self.led_controller.set_color(current_color)
        self.led_controller.show()

        if t >= 1.0:
            self.start_color = self.end_color
            self.end_color = color.random_rgb_255()
