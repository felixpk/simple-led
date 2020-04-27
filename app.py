import signal
from pathlib import Path

import pigpio
from flask import Flask, request, render_template

from animations import ANIMS
from colors.color import RGB255
from controllers.animation_controller import (
    AnimationController,
    AnimationNotFoundException
)
from controllers.led_controller import LedController
from helper.config import Config
from helper.log_manager import LogManager

APP = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            template_folder='templates')

CFG = Config.read(Path('config.yaml'))

PIGPIO = pigpio.pi(CFG['gpio']['host'],
                   CFG['gpio']['port'])

LED_CONTROLLER = LedController(PIGPIO,
                               CFG['led_strip']['spi_channel'],
                               CFG['led_strip']['spi_frequency'],
                               CFG['led_strip']['total_led_count'],
                               CFG['led_strip']['usable_led_count'])

ANIM_CONTROLLER = AnimationController(LED_CONTROLLER, Config(CFG['animations']))

AVAILABLE_ANIMATIONS = [(a, ANIMS[a].name) for a in ANIMS]

ANIMATION_OPTIONS = {
    "fade": [("duration", "float"), ("fps", "float")],
    "color_wheel": [("duration", "float")]
}

LOGMAN = LogManager('app')
LOGMAN.debug('Server started')


@APP.route('/api/color', methods=['POST'])
def set_color():
    ANIM_CONTROLLER.stop_current_animation()
    LED_CONTROLLER.set_color(RGB255(request.form.get('r'),
                                    request.form.get('g'),
                                    request.form.get('b')))
    LED_CONTROLLER.show()
    return {"status": "success"}


@APP.route('/api/disable', methods=['GET'])
def disable():
    ANIM_CONTROLLER.stop_current_animation()
    LED_CONTROLLER.set_color(RGB255(0, 0, 0))
    LED_CONTROLLER.show()
    return {"status": "success"}


@APP.route('/api/animation/start', methods=['POST'])
def start_animation():
    try:
        ANIM_CONTROLLER.start_animation(request.form.get('animation'), duration=2.0)
        return {"status": "success"}
    except AnimationNotFoundException as exc:
        return {"status": "error", "message": str(exc)}


@APP.route("/api/animation/options/<string:name>", methods=['GET'])
def animation_settings(name: str):
    if name in ANIMATION_OPTIONS:
        return {"options": ANIMATION_OPTIONS[name]}

    return {"status": "error"}


@APP.route('/api/animation/stop', methods=['GET'])
def stop_anaimation():
    ANIM_CONTROLLER.stop()
    return {"status": "success"}


@APP.route('/')
def home():
    return render_template('home.html', animations=AVAILABLE_ANIMATIONS)


def handle_signal(signum, frame):
    print(f"Signal Number {signum}, Frame {frame}")
    ANIM_CONTROLLER.stop()
    LED_CONTROLLER.close()
    PIGPIO.stop()

    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    APP.run(host='0.0.0.0')
