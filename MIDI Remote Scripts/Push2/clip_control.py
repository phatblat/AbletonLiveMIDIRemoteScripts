# Source Generated with Decompyle++
# File: clip_control.pyc (Python 2.5)

from ableton.v2.base import listens, liveobj_valid, listenable_property
from ableton.v2.control_surface import CompoundComponent
from ableton.v2.control_surface.control import ToggleButtonControl
from pushbase.clip_control_component import convert_length_to_bars_beats_sixteenths, convert_time_to_bars_beats_sixteenths, LoopSettingsControllerComponent as LoopSettingsControllerComponentBase, AudioClipSettingsControllerComponent as AudioClipSettingsControllerComponentBase, ONE_YEAR_AT_120BPM_IN_BEATS, WARP_MODE_NAMES
from clip_decoration import ClipDecoratorFactory
from decoration import find_decorated_object
from internal_parameter import WrappingParameter
from mapped_control import MappedControl
from real_time_channel import RealTimeDataComponent
from simpler_zoom import ZoomHandling
PARAMETERS_LOOPED = ('Loop position', 'Loop length', 'Start offset')
PARAMETERS_NOT_LOOPED = ('Start', 'End')
PARAMETERS_AUDIO = ('Warp', 'Transpose', 'Detune', 'Gain')

class LoopSetting(WrappingParameter):
    min = -ONE_YEAR_AT_120BPM_IN_BEATS
    max = ONE_YEAR_AT_120BPM_IN_BEATS
    
    def __init__(self, use_length_conversion = False, *a, **k):
        super(LoopSetting, self).__init__(*a, **a)
        if use_length_conversion:
            pass
        1
        self._conversion = convert_time_to_bars_beats_sixteenths
        self.recording = False

    
    def display_value(self):
        if not self.recording:
            pass
        1
        return unicode('...')

    display_value = property(display_value)


class ClipZoomHandling(ZoomHandling):
    
    def _set_zoom_parameter(self):
        self._zoom_parameter = getattr(self._parameter_host, '_zoom_parameter', None)

    
    def set_parameter_host(self, parameter_host):
        self._parameter_host = parameter_host
        self._set_zoom_parameter()
        if self._zoom_parameter:
            self._zoom_parameter.set_scaling_functions(self._zoom_to_internal, self._internal_to_zoom)
        
        self._on_zoom_changed.subject = self._zoom_parameter

    
    def max_zoom(self):
        clip = self._parameter_host
        if liveobj_valid(clip) and clip.length > 0:
            pass
        1
        length = clip.length(self.SCREEN_WIDTH)
        return float(length / self.SCREEN_WIDTH)

    max_zoom = property(max_zoom)


class LoopSettingsControllerComponent(LoopSettingsControllerComponentBase):
    __events__ = ('looping', 'loop_parameters', 'zoom')
    zoom_encoder = MappedControl()
    loop_button = ToggleButtonControl(toggled_color = 'Clip.Option', untoggled_color = 'Clip.OptionDisabled')
    
    def __init__(self, zoom_handler = None, *a, **k):
        super(LoopSettingsControllerComponent, self).__init__(*a, **a)
        self._looping_settings = [
            LoopSetting(name = PARAMETERS_LOOPED[0], parent = self._loop_model, source_property = 'position'),
            LoopSetting(name = PARAMETERS_LOOPED[1], parent = self._loop_model, use_length_conversion = True, source_property = 'loop_length'),
            LoopSetting(name = PARAMETERS_LOOPED[2], parent = self._loop_model, source_property = 'start_marker')]
        self._non_looping_settings = [
            LoopSetting(name = PARAMETERS_NOT_LOOPED[0], parent = self._loop_model, source_property = 'loop_start'),
            LoopSetting(name = PARAMETERS_NOT_LOOPED[1], parent = self._loop_model, source_property = 'loop_end')]
        for setting in self._looping_settings + self._non_looping_settings:
            self.register_disconnectable(setting)
        
        if not zoom_handler:
            pass
        self._zoom_handler = self.register_disconnectable(ClipZoomHandling())
        self._processed_zoom_requests = 0
        self._LoopSettingsControllerComponent__on_looping_changed.subject = self._loop_model
        self._LoopSettingsControllerComponent__on_looping_changed()

    
    def loop_button(self, toggled, button):
        self._loop_model.looping = toggled

    loop_button = loop_button.toggled(loop_button)
    
    def looping(self):
        if self.clip:
            pass
        1
        return False

    looping = property(looping)
    
    def loop_parameters(self):
        if not liveobj_valid(self.clip):
            return []
        
        if self.looping:
            pass
        1
        parameters = self._non_looping_settings
        if self.zoom:
            pass
        1
        return parameters

    loop_parameters = property(loop_parameters)
    
    def zoom(self):
        if liveobj_valid(self.clip):
            pass
        1

    zoom = property(zoom)
    
    def processed_zoom_requests(self):
        return self._processed_zoom_requests

    processed_zoom_requests = listenable_property(processed_zoom_requests)
    
    def __on_is_recording_changed(self):
        recording = False
        if liveobj_valid(self._loop_model.clip):
            recording = self._loop_model.clip.is_recording
            self._looping_settings[1].recording = recording
            self._non_looping_settings[1].recording = recording
        

    _LoopSettingsControllerComponent__on_is_recording_changed = listens('is_recording')(__on_is_recording_changed)
    
    def __on_looping_changed(self):
        self._update_and_notify()

    _LoopSettingsControllerComponent__on_looping_changed = listens('looping')(__on_looping_changed)
    
    def _update_loop_button(self):
        self.loop_button.enabled = liveobj_valid(self.clip)
        if liveobj_valid(self.clip):
            self.loop_button.is_toggled = self._loop_model.looping
        

    
    def _on_clip_changed(self):
        self._update_and_notify()
        self._LoopSettingsControllerComponent__on_is_recording_changed.subject = self._loop_model.clip
        self._LoopSettingsControllerComponent__on_is_recording_changed()
        self._zoom_handler.set_parameter_host(self._loop_model.clip)
        self._connect_encoder()

    
    def _update_and_notify(self):
        self._update_loop_button()
        self.notify_looping()
        self.notify_loop_parameters()
        self.notify_zoom()

    
    def _connect_encoder(self):
        self.zoom_encoder.mapped_parameter = self.zoom

    
    def set_zoom_encoder(self, encoder):
        self.zoom_encoder.set_control_element(encoder)
        self._connect_encoder()

    
    def request_zoom(self, zoom_factor):
        self._zoom_handler.request_zoom(zoom_factor)
        self._processed_zoom_requests += 1
        self.notify_processed_zoom_requests()



class GainSetting(WrappingParameter):
    
    def display_value(self):
        if self._parent.clip:
            pass
        1
        return self._parent.clip.gain_display_string('')

    display_value = property(display_value)


class PitchSetting(WrappingParameter):
    
    def __init__(self, min_value, max_value, unit, *a, **k):
        super(PitchSetting, self).__init__(*a, **a)
        self._min = min_value
        self._max = max_value
        self._unit = unit

    
    def min(self):
        return self._min

    min = property(min)
    
    def max(self):
        return self._max

    max = property(max)
    
    def display_value(self):
        value = int(round(float(self._get_property_value())))
        if value > 0:
            pass
        1
        positive_indicator = ''
        return positive_indicator + str(value) + self._unit

    display_value = property(display_value)


class WarpSetting(WrappingParameter):
    
    def max(self):
        return len(self._parent.available_warp_modes) - 1

    max = property(max)
    
    def is_quantized(self):
        return True

    is_quantized = property(is_quantized)
    
    def value_items(self):
        return map(lambda x: unicode(WARP_MODE_NAMES[x]), self._parent.available_warp_modes)

    value_items = property(value_items)
    
    def _get_property_value(self):
        return self._parent.available_warp_modes.index(getattr(self._parent, self._source_property))



class AudioClipSettingsControllerComponent(AudioClipSettingsControllerComponentBase, CompoundComponent):
    __events__ = ('audio_parameters', 'warping', 'gain')
    
    def __init__(self, *a, **k):
        super(AudioClipSettingsControllerComponent, self).__init__(*a, **a)
        self._audio_clip_parameters = [
            WarpSetting(name = PARAMETERS_AUDIO[0], parent = self._audio_clip_model, source_property = 'warp_mode'),
            PitchSetting(name = PARAMETERS_AUDIO[1], parent = self._audio_clip_model, source_property = 'pitch_coarse', min_value = -49, max_value = 49, unit = 'st'),
            PitchSetting(name = PARAMETERS_AUDIO[2], parent = self._audio_clip_model, source_property = 'pitch_fine', min_value = -51, max_value = 51, unit = 'ct'),
            GainSetting(name = PARAMETERS_AUDIO[3], parent = self._audio_clip_model, source_property = 'gain')]
        self._playhead_real_time_data = self.register_component(RealTimeDataComponent(channel_type = 'playhead'))
        self._waveform_real_time_data = self.register_component(RealTimeDataComponent(channel_type = 'waveform'))
        for parameter in self._audio_clip_parameters:
            self.register_disconnectable(parameter)
        
        self._AudioClipSettingsControllerComponent__on_warping_changed.subject = self._audio_clip_model
        self._AudioClipSettingsControllerComponent__on_gain_changed.subject = self._audio_clip_model
        self._AudioClipSettingsControllerComponent__on_warping_changed()
        self._AudioClipSettingsControllerComponent__on_gain_changed()

    
    def disconnect(self):
        super(AudioClipSettingsControllerComponent, self).disconnect()
        self._playhead_real_time_data.set_data(None)
        self._waveform_real_time_data.set_data(None)

    
    def audio_parameters(self):
        if liveobj_valid(self.clip):
            pass
        1
        return []

    audio_parameters = property(audio_parameters)
    
    def warping(self):
        if liveobj_valid(self.clip):
            pass
        1
        return False

    warping = property(warping)
    
    def gain(self):
        if liveobj_valid(self.clip):
            pass
        1
        return 0

    gain = property(gain)
    
    def waveform_real_time_channel_id(self):
        return self._waveform_real_time_data.channel_id

    waveform_real_time_channel_id = property(waveform_real_time_channel_id)
    
    def playhead_real_time_channel_id(self):
        return self._playhead_real_time_data.channel_id

    playhead_real_time_channel_id = property(playhead_real_time_channel_id)
    
    def _on_clip_changed(self):
        self._playhead_real_time_data.set_data(self.clip)
        self._waveform_real_time_data.set_data(self.clip)
        self.notify_audio_parameters()
        self.notify_warping()
        self.notify_gain()

    
    def _on_transpose_encoder_value(self, value):
        self._audio_clip_model.set_clip_pitch_coarse(value, False)

    
    def _on_detune_encoder_value(self, value):
        self._audio_clip_model.set_clip_pitch_fine(value, False)

    
    def __on_warping_changed(self):
        self.notify_warping()

    _AudioClipSettingsControllerComponent__on_warping_changed = listens('warping')(__on_warping_changed)
    
    def __on_gain_changed(self):
        self.notify_gain()

    _AudioClipSettingsControllerComponent__on_gain_changed = listens('gain')(__on_gain_changed)


class ClipControlComponent(CompoundComponent):
    __events__ = ('clip',)
    
    def __init__(self, loop_controller = None, audio_clip_controller = None, mode_selector = None, decorator_factory = None, *a, **k):
        if not loop_controller is not None:
            raise AssertionError
        if not audio_clip_controller is not None:
            raise AssertionError
        if not mode_selector is not None:
            raise AssertionError
        super(ClipControlComponent, self).__init__(*a, **a)
        self._loop_controller = self.register_component(loop_controller)
        self._audio_clip_controller = self.register_component(audio_clip_controller)
        self._mode_selector = self.register_component(mode_selector)
        if not decorator_factory:
            pass
        self._decorator_factory = ClipDecoratorFactory()
        self._ClipControlComponent__on_selected_clip_changed.subject = self.song.view
        self._ClipControlComponent__on_selected_clip_changed()

    
    def __on_selected_clip_changed(self):
        self._update_controller()

    _ClipControlComponent__on_selected_clip_changed = listens('detail_clip')(__on_selected_clip_changed)
    
    def on_enabled_changed(self):
        super(ClipControlComponent, self).on_enabled_changed()
        self._update_controller()

    
    def _decorate_clip(self, clip):
        if not find_decorated_object(clip, self._decorator_factory):
            pass
        return self._decorator_factory.decorate(clip)

    
    def _update_controller(self):
        if self.is_enabled():
            clip = self.song.view.detail_clip
            self._update_selected_mode(clip)
            if self._mode_selector.selected_mode == 'audio':
                pass
            1
            self._loop_controller.clip = clip
            if liveobj_valid(clip) and clip.is_audio_clip:
                pass
            1
            self._audio_clip_controller.clip = None
            self.notify_clip()
        

    
    def _update_selected_mode(self, clip):
        if liveobj_valid(clip):
            if clip.is_audio_clip:
                pass
            1
            self._mode_selector.selected_mode = 'midi'
        else:
            self._mode_selector.selected_mode = 'no_clip'

    
    def clip(self):
        return self._loop_controller.clip

    clip = property(clip)

