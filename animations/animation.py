import time
from abc import ABC, abstractmethod
from enum import Enum
from threading import Thread, Event

from helper.config import Config
from controllers.led_controller import LedController


class LoopMode(Enum):
    SINGLE = 0
    ENDLESS = 1


class Animation(ABC, Thread):
    name = 'None'

    def __init__(self, led_controller: LedController):
        super().__init__()

        # stops the animation thred if set
        self._stop_event: Event = Event()

        # interface to communicate with rbp leds
        self.led_controller: LedController = led_controller

        # How many times the animation should update per second
        self.target_frame_rate: float = 10.0

        # animation duration in seconds
        self.duration: float = 10.0

        # animation progress in percent [0-1]
        self.anim_progress: float = 0.0

        # Looping mode of the animation
        self.loop_mode: LoopMode = LoopMode.SINGLE

        # how long this animation is running
        self.elapsed_anim_time = 0

    def run(self):
        self.on_start()

        current_lerp_time = 0
        last_update = time.time()

        while not self._stop_event.is_set():
            update_start = time.time()
            delta_time = update_start - last_update
            last_update = update_start

            current_lerp_time += delta_time
            if current_lerp_time > self.duration:
                current_lerp_time = self.duration

            self.elapsed_anim_time += delta_time

            self.anim_progress = current_lerp_time / self.duration

            self.on_update()

            if current_lerp_time == self.duration:
                if self.loop_mode == LoopMode.SINGLE:
                    self.stop()
                elif self.loop_mode == LoopMode.ENDLESS:
                    current_lerp_time = 0

            sleep = (1.0 / self.target_frame_rate) - (time.time() - update_start)
            if sleep > 0:
                time.sleep(sleep)

        self.on_stop()

    def stop(self):
        self._stop_event.set()
        self.join()

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_stop(self):
        pass

    @abstractmethod
    def on_update(self):
        pass
