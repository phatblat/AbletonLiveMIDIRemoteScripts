# Source Generated with Decompyle++
# File: track_mixer_control_component.pyc (Python 2.5)

from ableton.v2.base import clamp, depends, listens, liveobj_valid
from ableton.v2.control_surface import CompoundComponent
from ableton.v2.control_surface.control import control_list, ButtonControl
from mapped_control import MappedControl
from real_time_channel import RealTimeDataComponent
from item_lister_component import SimpleItemSlot
MAX_RETURN_TRACKS = 6

class TrackMixerControlComponent(CompoundComponent):
    __events__ = ('parameters', 'scroll_offset', 'items')
    BUTTON_SKIN = dict(color = 'TrackControlView.ButtonOff', pressed_color = 'TrackControlView.ButtonOn', disabled_color = 'TrackControlView.ButtonDisabled')
    controls = control_list(MappedControl)
    scroll_right_button = ButtonControl(**None)
    scroll_left_button = ButtonControl(**None)
    
    def __init__(self, real_time_mapper = None, register_real_time_data = None, tracks_provider = None, *a, **k):
        if not liveobj_valid(real_time_mapper):
            raise AssertionError
        if not tracks_provider is not None:
            raise AssertionError
        super(TrackMixerControlComponent, self).__init__(*a, **a)
        self._tracks_provider = tracks_provider
        self._on_return_tracks_changed.subject = self.song
        self.real_time_meter_channel = self.register_component(RealTimeDataComponent(real_time_mapper = real_time_mapper, register_real_time_data = register_real_time_data, channel_type = 'meter'))
        self._scroll_offset = 0
        self._items = []
        self._number_return_tracks = self._number_sends()
        self._update_scroll_buttons()
        self._TrackMixerControlComponent__on_selected_item_changed.subject = self._tracks_provider

    __init__ = depends(tracks_provider = None, real_time_mapper = None, register_real_time_data = None)(__init__)
    
    def set_controls(self, controls):
        self.controls.set_control_element(controls)
        self._update_controls()

    
    def __on_selected_item_changed(self):
        self._update_scroll_offset()
        self._update_real_time_channel_id()

    _TrackMixerControlComponent__on_selected_item_changed = listens('selected_item')(__on_selected_item_changed)
    
    def update(self):
        super(TrackMixerControlComponent, self).update()
        if self.is_enabled():
            self._update_controls()
            self._update_scroll_buttons()
            self._update_real_time_channel_id()
        

    
    def _update_real_time_channel_id(self):
        self.real_time_meter_channel.set_data(self._tracks_provider.selected_item.mixer_device)

    
    def _update_controls(self):
        if self.is_enabled():
            for (control, parameter) in map(None, self.controls, self.parameters[self.scroll_offset:]):
                if control:
                    control.mapped_parameter = parameter
                    continue
            
            self.notify_parameters()
        

    
    def parameters(self):
        return self._get_track_mixer_parameters()

    parameters = property(parameters)
    
    def scroll_offset(self):
        return self._scroll_offset

    scroll_offset = property(scroll_offset)
    
    def _on_return_tracks_changed(self):
        self._update_controls()
        self._update_scroll_offset()

    _on_return_tracks_changed = listens('return_tracks')(_on_return_tracks_changed)
    
    def _number_sends(self):
        mixable = self._tracks_provider.selected_item
        if mixable != self.song.master_track:
            pass
        1
        return 0

    
    def _update_scroll_offset(self):
        new_number_return_tracks = self._number_sends()
        if MAX_RETURN_TRACKS <= new_number_return_tracks:
            pass
        new_number_return_tracks < self._number_return_tracks
        if 1 and MAX_RETURN_TRACKS + self._scroll_offset > new_number_return_tracks:
            delta = min(new_number_return_tracks - self._number_return_tracks, 0)
            self._scroll_controls(delta)
        elif new_number_return_tracks < MAX_RETURN_TRACKS or self._tracks_provider.selected_item == self.song.master_track:
            self._scroll_offset = 0
        
        self._update_controls()
        self._update_scroll_buttons()
        self._number_return_tracks = new_number_return_tracks

    
    def _get_track_mixer_parameters(self):
        mixer_params = []
        if self._tracks_provider.selected_item:
            mixer = self._tracks_provider.selected_item.mixer_device
            mixer_params = [
                mixer.volume,
                mixer.panning] + list(mixer.sends)
        
        return mixer_params

    
    def scroll_right_button(self, button):
        self._scroll_controls(1)

    scroll_right_button = scroll_right_button.pressed(scroll_right_button)
    
    def scroll_left_button(self, button):
        self._scroll_controls(-1)

    scroll_left_button = scroll_left_button.pressed(scroll_left_button)
    
    def _update_scroll_buttons(self):
        if self.is_enabled():
            num_return_tracks = self._number_sends()
            self.scroll_right_button.enabled = num_return_tracks > MAX_RETURN_TRACKS + self._scroll_offset
            self.scroll_left_button.enabled = self._scroll_offset > 0
            self._update_view_slots()
        

    
    def items(self):
        return self._items

    items = property(items)
    
    def _update_view_slots(self):
        continue
        self._items = [ SimpleItemSlot() for _ in xrange(6) ]
        if self.scroll_left_button.enabled:
            pass
        1
        SimpleItemSlot('icon'(page_left.svg = ''))
        if self.scroll_right_button.enabled:
            pass
        1
        SimpleItemSlot('icon'(page_right.svg = ''))
        self.notify_items()

    
    def _scroll_controls(self, delta):
        num_return_tracks = self._number_sends()
        if num_return_tracks > MAX_RETURN_TRACKS:
            pass
        1
        self._scroll_offset = self._scroll_offset + delta(0, num_return_tracks, 0)
        self.notify_scroll_offset()
        self._update_controls()
        self._update_scroll_buttons()


