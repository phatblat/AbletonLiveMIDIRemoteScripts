# Source Generated with Decompyle++
# File: setup_component.pyc (Python 2.5)

from ableton.v2.base import CompoundDisconnectable, SerializableListenableProperties, Subject, clamp, listenable_property
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import RadioButtonControl, StepEncoderControl, ToggleButtonControl, control_list
from ableton.v2.control_surface.mode import ModesComponent
from pad_velocity_curve import PadVelocityCurveSettings
PAD_SETTING_STEP_SIZE = 20
MIN_USER_FACING_LED_BRIGHTNESS = 13
MIN_USER_FACING_DISPLAY_BRIGHTNESS = 2

class GeneralSettings(Subject):
    workflow = listenable_property.managed('scene')


class HardwareSettings(SerializableListenableProperties):
    min_led_brightness = MIN_USER_FACING_LED_BRIGHTNESS
    max_led_brightness = 127
    led_brightness = listenable_property.managed(max_led_brightness)
    min_display_brightness = MIN_USER_FACING_DISPLAY_BRIGHTNESS
    max_display_brightness = 255
    display_brightness = listenable_property.managed(max_display_brightness)


class DisplayDebugSettings(SerializableListenableProperties):
    show_row_spaces = listenable_property.managed(False)
    show_row_margins = listenable_property.managed(False)
    show_row_middle = listenable_property.managed(False)
    show_button_spaces = listenable_property.managed(False)
    show_unlit_button = listenable_property.managed(False)
    show_lit_button = listenable_property.managed(False)


class ProfilingSettings(SerializableListenableProperties):
    show_qml_stats = listenable_property.managed(False)
    show_usb_stats = listenable_property.managed(False)
    show_realtime_ipc_stats = listenable_property.managed(False)


class Settings(CompoundDisconnectable):
    
    def __init__(self, preferences = None, *a, **k):
        if not preferences is not None:
            raise AssertionError
        super(Settings, self).__init__(*a, **a)
        self._general = self.register_disconnectable(GeneralSettings())
        self._pad_settings = self.register_disconnectable(preferences.setdefault('settings_pad_velocity_curve', PadVelocityCurveSettings()))
        self._hardware = self.register_disconnectable(preferences.setdefault('settings_hardware', HardwareSettings()))
        self._display_debug = self.register_disconnectable(preferences.setdefault('settings_display_debug', DisplayDebugSettings()))
        self._profiling = self.register_disconnectable(preferences.setdefault('settings_profiling', ProfilingSettings()))

    
    def general(self):
        return self._general

    general = property(general)
    
    def pad_settings(self):
        return self._pad_settings

    pad_settings = property(pad_settings)
    
    def hardware(self):
        return self._hardware

    hardware = property(hardware)
    
    def display_debug(self):
        return self._display_debug

    display_debug = property(display_debug)
    
    def profiling(self):
        return self._profiling

    profiling = property(profiling)


class GeneralSettingsComponent(Component):
    workflow_encoder = StepEncoderControl()
    led_brightness_encoder = StepEncoderControl(num_steps = 60)
    display_brightness_encoder = StepEncoderControl(num_steps = 120)
    
    def __init__(self, settings = None, hardware_settings = None, *a, **k):
        if not settings is not None:
            raise AssertionError
        if not hardware_settings is not None:
            raise AssertionError
        super(GeneralSettingsComponent, self).__init__(*a, **a)
        self._settings = settings
        self._hardware_settings = hardware_settings
        self.workflow_encoder.connect_property(settings, 'workflow', lambda v: if v > 0:
pass1'scene')

    
    def led_brightness_encoder(self, value, encoder):
        self._hardware_settings.led_brightness = clamp(self._hardware_settings.led_brightness + value, self._hardware_settings.min_led_brightness, self._hardware_settings.max_led_brightness)

    led_brightness_encoder = led_brightness_encoder.value(led_brightness_encoder)
    
    def display_brightness_encoder(self, value, encoder):
        self._hardware_settings.display_brightness = clamp(self._hardware_settings.display_brightness + value, self._hardware_settings.min_display_brightness, self._hardware_settings.max_display_brightness)

    display_brightness_encoder = display_brightness_encoder.value(display_brightness_encoder)


class PadSettingsComponent(Component):
    sensitivity_encoder = StepEncoderControl(num_steps = PAD_SETTING_STEP_SIZE)
    gain_encoder = StepEncoderControl(num_steps = PAD_SETTING_STEP_SIZE)
    dynamics_encoder = StepEncoderControl(num_steps = PAD_SETTING_STEP_SIZE)
    
    def __init__(self, pad_settings = None, hardware_settings = None, *a, **k):
        if not pad_settings is not None:
            raise AssertionError
        super(PadSettingsComponent, self).__init__(*a, **a)
        self._pad_settings = pad_settings

    
    def sensitivity_encoder(self, value, encoder):
        self._pad_settings.sensitivity = clamp(self._pad_settings.sensitivity + value, self._pad_settings.min_sensitivity, self._pad_settings.max_sensitivity)

    sensitivity_encoder = sensitivity_encoder.value(sensitivity_encoder)
    
    def gain_encoder(self, value, encoder):
        self._pad_settings.gain = clamp(self._pad_settings.gain + value, self._pad_settings.min_gain, self._pad_settings.max_gain)

    gain_encoder = gain_encoder.value(gain_encoder)
    
    def dynamics_encoder(self, value, encoder):
        self._pad_settings.dynamics = clamp(self._pad_settings.dynamics + value, self._pad_settings.min_dynamics, self._pad_settings.max_dynamics)

    dynamics_encoder = dynamics_encoder.value(dynamics_encoder)


class DisplayDebugSettingsComponent(Component):
    show_row_spaces_button = ToggleButtonControl()
    show_row_margins_button = ToggleButtonControl()
    show_row_middle_button = ToggleButtonControl()
    show_button_spaces_button = ToggleButtonControl()
    show_unlit_button_button = ToggleButtonControl()
    show_lit_button_button = ToggleButtonControl()
    
    def __init__(self, settings = None, *a, **k):
        if not settings is not None:
            raise AssertionError
        super(DisplayDebugSettingsComponent, self).__init__(*a, **a)
        self.show_row_spaces_button.connect_property(settings, 'show_row_spaces')
        self.show_row_margins_button.connect_property(settings, 'show_row_margins')
        self.show_row_middle_button.connect_property(settings, 'show_row_middle')
        self.show_button_spaces_button.connect_property(settings, 'show_button_spaces')
        self.show_unlit_button_button.connect_property(settings, 'show_unlit_button')
        self.show_lit_button_button.connect_property(settings, 'show_lit_button')



class ProfilingSettingsComponent(Component):
    show_qml_stats_button = ToggleButtonControl()
    show_usb_stats_button = ToggleButtonControl()
    show_realtime_ipc_stats_button = ToggleButtonControl()
    
    def __init__(self, settings = None, *a, **k):
        if not settings is not None:
            raise AssertionError
        super(ProfilingSettingsComponent, self).__init__(*a, **a)
        self.show_qml_stats_button.connect_property(settings, 'show_qml_stats')
        self.show_usb_stats_button.connect_property(settings, 'show_usb_stats')
        self.show_realtime_ipc_stats_button.connect_property(settings, 'show_realtime_ipc_stats')



class SetupComponent(ModesComponent):
    category_radio_buttons = control_list(RadioButtonControl, checked_color = 'Option.Selected', unchecked_color = 'Option.Unselected')
    
    def __init__(self, settings = None, pad_curve_sender = None, in_developer_mode = False, *a, **k):
        if not settings is not None:
            raise AssertionError
        super(SetupComponent, self).__init__(*a, **a)
        self._settings = settings
        self._pad_curve_sender = pad_curve_sender
        self._general = self.register_component(GeneralSettingsComponent(settings = settings.general, hardware_settings = settings.hardware, is_enabled = False))
        self._pad_settings = self.register_component(PadSettingsComponent(pad_settings = settings.pad_settings, is_enabled = False))
        self._display_debug = self.register_component(DisplayDebugSettingsComponent(settings = settings.display_debug, is_enabled = False))
        self._profiling = self.register_component(ProfilingSettingsComponent(settings = settings.profiling, is_enabled = False))
        self.add_mode('Settings', [
            self._general,
            self._pad_settings])
        self.add_mode('Info', [])
        if in_developer_mode:
            self.add_mode('Display Debug', [
                self._display_debug])
            self.add_mode('Profiling', [
                self._profiling])
        
        self.selected_mode = 'Settings'
        self.category_radio_buttons.control_count = len(self.modes)
        self.category_radio_buttons.checked_index = 0

    
    def general(self):
        return self._general

    general = property(general)
    
    def pad_settings(self):
        return self._pad_settings

    pad_settings = property(pad_settings)
    
    def display_debug(self):
        return self._display_debug

    display_debug = property(display_debug)
    
    def profiling(self):
        return self._profiling

    profiling = property(profiling)
    
    def settings(self):
        return self._settings

    settings = property(settings)
    
    def velocity_curve(self):
        return self._pad_curve_sender

    velocity_curve = property(velocity_curve)
    
    def category_radio_buttons(self, button):
        self.selected_mode = self.modes[button.index]

    category_radio_buttons = category_radio_buttons.checked(category_radio_buttons)

