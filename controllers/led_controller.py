import pigpio

from colors.color import RGB255


class LedController:
    def __init__(self, gpio_controller: pigpio.pi, spi_channel, spi_frequency,
                 total_led_count, usable_led_count):

        """
        WS2801 Addressable LED controller

        :param gpio_controller:
        :param spi_channel: SPI channel (0-1)
        :param total_led_count: Number of LEDs on the strip
        :param usable_led_count: Number of LEDs to use
        """

        self.gpio_controller = gpio_controller
        self.spi_channel = spi_channel
        self.spi_frequency = spi_frequency
        self.total_led_count = total_led_count
        self.usable_led_count = usable_led_count

        self.colors = [0] * (total_led_count * 3)
        self.spi_dev = self.gpio_controller.spi_open(spi_channel, spi_frequency)

    def set_single_color(self, index: int, color: RGB255):
        self.colors[index * 3] = color.r
        self.colors[index * 3 + 2] = color.g
        self.colors[index * 3 + 1] = color.b

    def set_color(self, color: RGB255):
        self.colors = list((color.r, color.b, color.g) * self.usable_led_count) + [0] * 3 * (self.total_led_count - self.usable_led_count)

    def clear(self) -> None:
        """Zeroes the color array."""
        self.colors = [0] * (self.total_led_count * 3)

    def sclear(self):
        """
        Zeroes the color array and writes to gpio.

        Shorthand for clear() followed by show()
        """
        self.colors = [0] * (self.total_led_count * 3)
        self.show()

    def show(self):
        """Writes colors in color array to gpio."""
        self.gpio_controller.spi_write(self.spi_dev, self.colors)

    def close(self):
        self.gpio_controller.spi_close(self.spi_dev)
