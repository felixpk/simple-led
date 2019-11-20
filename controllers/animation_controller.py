from typing import Union

from animations import ANIMATIONS
from animations.animation import Animation
from helper.config import Config
from controllers.led_controller import LedController


class AnimationController:
    def __init__(self, led_controller: LedController, config: Config):
        self.led_controller = led_controller
        self.config = config
        self.current_animation: Union[Animation, None] = None

    def start_animation(self, animation_name: str):
        anim_cfg = self.config.get(animation_name, {})

        try:
            self.stop_current_animation()
            self.current_animation = ANIMATIONS[animation_name](
                self.led_controller, anim_cfg)
            self.current_animation.start()
        except KeyError:
            raise AnimationNotFoundException(f"'{animation_name}' was not found")

    def stop_current_animation(self):
        if self.current_animation:
            self.current_animation.stop()
            self.current_animation = None

    def stop(self):
        self.stop_current_animation()


class AnimationNotFoundException(Exception):
    pass
