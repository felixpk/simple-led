from typing import Tuple, List
from colors.color import RGB255

import pigpio


class LedController:
    def __init__(self, gpio_controller: pigpio.pi,
                 spi_channel,
                 spi_frequency, total_led_count,
                 usable_led_count):
        """
        WS2801 Addressable LED controller

        :param gpio_controller:
        :param spi_channel: SPI channel (0-1)
        :param total_led_count: Number of LEDs to use
        """
        self.gpio_controller = gpio_controller
        self.spi_channel = spi_channel
        self.spi_frequency = spi_frequency
        self.total_led_count = total_led_count
        self.usable_led_count = usable_led_count

        self.colors = [0] * (total_led_count * 3)
        self.spi_dev = self.gpio_controller.spi_open(spi_channel, spi_frequency, 0)

    def set_single_color(self, index: int, color: RGB255):
        self.colors[index * 3] = color.r
        self.colors[index * 3 + 2] = color.g
        self.colors[index * 3 + 1] = color.b

    def set_color(self, color: RGB255):
        self.colors = list((int(color.r), int(color.b), int(color.g)) * self.usable_led_count) + \
                      ([0] * 3 * (self.total_led_count - self.usable_led_count))

    def set_colors(self, colors: List[RGB255]):
        res = list()
        for c in colors:
            res.append(c.r)
            res.append(c.b)
            res.append(c.g)
        self.colors = res

    def clear(self):
        self.colors = [0] * (self.total_led_count * 3)

    def show(self):
        self.gpio_controller.spi_write(self.spi_dev, self.colors)

    def close(self):
        self.gpio_controller.spi_close(self.spi_dev)
