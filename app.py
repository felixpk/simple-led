import signal
from pathlib import Path

import pigpio
from flask import Flask, request

from auxiliary.config import Config
from colors.color import RGB255
from controllers.animation_controller import (
    AnimationController,
    AnimationNotFoundException
)
from controllers.led_controller import LedController

APP = Flask(__name__)

CFG = Config.read(Path('config.yml'))

PIGPIO = pigpio.pi(CFG['gpio']['host'],
                   CFG['gpio']['port'])

LED_CONTROLLER = LedController(PIGPIO,
                               CFG['led_strip']['spi_channel'],
                               CFG['led_strip']['spi_frequency'],
                               CFG['led_strip']['total_led_count'],
                               CFG['led_strip']['usable_led_count'])

ANIM_CONTROLLER = AnimationController(LED_CONTROLLER, Config(CFG['animations']))


@APP.route('/api/color', methods=['GET'])
def set_color():
    ANIM_CONTROLLER.stop_current_animation()
    LED_CONTROLLER.set_color(RGB255(request.args.get('r'),
                                    request.args.get('g'),
                                    request.args.get('b')))
    LED_CONTROLLER.show()
    return {"status": "success"}


@APP.route('/api/disable', methods=['GET'])
def disable():
    ANIM_CONTROLLER.stop_current_animation()
    LED_CONTROLLER.set_color(RGB255(0, 0, 0))
    LED_CONTROLLER.show()
    return {"status": "success"}


@APP.route('/api/animation/start', methods=['GET'])
def start_animation():
    try:
        ANIM_CONTROLLER.start_animation(request.args.get('name'))
        return {"status": "success"}
    except AnimationNotFoundException as exc:
        return {"status": "error", "message": str(exc)}


@APP.route('/api/animation/stop', methods=['GET'])
def stop_anaimation():
    ANIM_CONTROLLER.stop()
    return {"status": "success"}


@APP.route('/')
def home():
    return "<h1>Home</h1>"


def handle_signal(signum, frame):
    print(f"Signal Number {signum}, Frame {frame}")
    ANIM_CONTROLLER.stop()
    LED_CONTROLLER.close()
    PIGPIO.stop()

    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    APP.run(debug=False)
