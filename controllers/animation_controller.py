from typing import Union

from animations import ANIMS
from animations.animation import Animation
from controllers.led_controller import LedController
from helper.config import Config
from helper.log_manager import LogManager

LOG = LogManager(__name__)


class AnimationController:
    def __init__(self, led_controller: LedController, config: Config):
        self.led_controller = led_controller
        self.config = config
        self.current_animation: Union[Animation, None] = None

    def start_animation(self, name: str, **kwargs):
        print(f"Inside start_animation: {kwargs.items()}")

        try:
            self.stop_current_animation()
            self.current_animation = ANIMS[name](self.led_controller, **kwargs)
            self.current_animation.start()
        except KeyError:
            raise AnimationNotFoundException(f"'{name}' was not found")

    def stop_current_animation(self):
        if self.current_animation:
            self.current_animation.stop()
            self.current_animation = None

    def stop(self):
        self.stop_current_animation()


class AnimationNotFoundException(Exception):
    pass
