# Source Generated with Decompyle++
# File: hardware_settings_component.pyc (Python 2.5)

import Live
from ableton.v2.base import clamp, listens, task
from ableton.v2.control_surface import Component
LED_FADE_IN_DELAY = 0.3
LED_FADE_IN_TIME = 200
LED_FADE_IN_FREQUENCY = 16
MIN_BRIGHTNESS_FOR_FADE_IN = 0

class HardwareSettingsComponent(Component):
    
    def __init__(self, led_brightness_element = None, display_brightness_element = None, settings = None, *a, **k):
        if not led_brightness_element is not None:
            raise AssertionError
        if not display_brightness_element is not None:
            raise AssertionError
        if not settings is not None:
            raise AssertionError
        super(HardwareSettingsComponent, self).__init__(*a, **a)
        self._settings = settings
        self._led_brightness_element = led_brightness_element
        self._display_brightness_element = display_brightness_element
        self._led_brightness_timer = Live.Base.Timer(callback = self._on_fade_in_led_brightness_timer, interval = LED_FADE_IN_FREQUENCY, repeat = True)
        self._target_led_brightness = 0
        self._led_brightness = 0
        self._fade_in_delay_task = self._tasks.add(task.sequence(task.wait(LED_FADE_IN_DELAY), task.run(self._led_brightness_timer.restart))).kill()
        self._HardwareSettingsComponent__on_led_brightness_changed.subject = settings
        self._HardwareSettingsComponent__on_display_brightness_changed.subject = settings

    
    def disconnect(self):
        super(HardwareSettingsComponent, self).disconnect()
        self._led_brightness_timer.stop()
        self._led_brightness_timer = None

    
    def fade_in_led_brightness(self, target_brightness):
        if MIN_BRIGHTNESS_FOR_FADE_IN <= target_brightness:
            pass
        target_brightness <= self._settings.max_led_brightness
        if not 1:
            raise AssertionError
        self._led_brightness = MIN_BRIGHTNESS_FOR_FADE_IN
        self._target_led_brightness = target_brightness
        self._led_brightness_element.send_value(MIN_BRIGHTNESS_FOR_FADE_IN)
        self._fade_in_delay_task.restart()

    
    def stop_fade_in_led_brightness(self):
        self._led_brightness_timer.stop()
        self._led_brightness = MIN_BRIGHTNESS_FOR_FADE_IN
        self._target_led_brightness = MIN_BRIGHTNESS_FOR_FADE_IN
        self._fade_in_delay_task.kill()

    
    def _on_fade_in_led_brightness_timer(self):
        if self._led_brightness < self._target_led_brightness:
            distance = float(self._target_led_brightness - MIN_BRIGHTNESS_FOR_FADE_IN)
            increment = (distance / LED_FADE_IN_TIME) * LED_FADE_IN_FREQUENCY
            self._led_brightness = clamp(self._led_brightness + increment, MIN_BRIGHTNESS_FOR_FADE_IN, self._target_led_brightness)
            self._led_brightness_element.send_value(int(round(self._led_brightness)))
        else:
            self._led_brightness_timer.stop()

    
    def __on_led_brightness_changed(self, value):
        self.stop_fade_in_led_brightness()
        self._led_brightness_element.send_value(value)

    _HardwareSettingsComponent__on_led_brightness_changed = listens('led_brightness')(__on_led_brightness_changed)
    
    def __on_display_brightness_changed(self, value):
        self._display_brightness_element.send_value(value)

    _HardwareSettingsComponent__on_display_brightness_changed = listens('display_brightness')(__on_display_brightness_changed)
    
    def send(self):
        self.stop_fade_in_led_brightness()
        self._led_brightness_element.send_value(self._settings.led_brightness)
        self._display_brightness_element.send_value(self._settings.display_brightness)


