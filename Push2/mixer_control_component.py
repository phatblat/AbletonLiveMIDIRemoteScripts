# Source Generated with Decompyle++
# File: mixer_control_component.pyc (Python 2.5)

from __future__ import with_statement
from contextlib import contextmanager
from functools import partial
from itertools import izip
from math import ceil
from ableton.v2.base import clamp, depends, listens, liveobj_valid, NamedTuple
from ableton.v2.control_surface.control import control_list, ButtonControl
from ableton.v2.control_surface.mode import ModesComponent
from mapped_control import MappedControl
from real_time_channel import RealTimeDataComponent
from item_lister_component import SimpleItemSlot
MIXER_SECTIONS = ('Volumes', 'Pans')
SEND_SECTIONS = [
    'A Sends',
    'B Sends',
    'C Sends',
    'D Sends',
    'E Sends',
    'F Sends',
    'G Sends',
    'H Sends',
    'I Sends',
    'J Sends',
    'K Sends',
    'L Sends']
SEND_LIST_LENGTH = 5
SEND_MODE_NAMES = [
    'send_slot_one',
    'send_slot_two',
    'send_slot_three',
    'send_slot_four',
    'send_slot_five']

class MixerSectionDescription(NamedTuple):
    view = None
    parameter_name = None


class MixerControlComponent(ModesComponent):
    __events__ = ('items', 'selected_item')
    controls = control_list(MappedControl)
    cycle_sends_button = ButtonControl(color = 'DefaultButton.Off')
    
    def __init__(self, view_model = None, tracks_provider = None, real_time_mapper = None, register_real_time_data = None, *a, **k):
        if not liveobj_valid(real_time_mapper):
            raise AssertionError
        if not view_model is not None:
            raise AssertionError
        if not tracks_provider is not None:
            raise AssertionError
        super(MixerControlComponent, self).__init__(*a, **a)
        self._send_offset = 0
        continue
        self.real_time_meter_handlers = [ RealTimeDataComponent(channel_type = 'meter', real_time_mapper = real_time_mapper, register_real_time_data = register_real_time_data, is_enabled = False) for _ in xrange(8) ]
        self._track_provider = tracks_provider
        self._on_return_tracks_changed.subject = self.song
        self._on_mode_changed.subject = self
        self._mixer_section_view = None
        self._mixer_sections = []
        self._selected_view = view_model.volumeControlListView
        
        self._parameter_getter = lambda x: pass
        self._setup_modes(view_model)
        self.selected_mode = 'volume'
        self._selected_item = ''
        self._items = []
        self._on_return_tracks_changed()
        self._update_mixer_sections()
        self._on_items_changed.subject = self._track_provider
        self._on_selected_item_changed.subject = self._track_provider

    __init__ = depends(tracks_provider = None, real_time_mapper = None, register_real_time_data = None)(__init__)
    
    def _setup_modes(self, view_model):
        self._add_mode('volume', view_model.volumeControlListView, lambda mixer: mixer.volume, additional_mode_contents = self.real_time_meter_handlers)
        self._add_mode('panning', view_model.panControlListView, lambda mixer: mixer.panning)
        
        def add_send_mode(index):
            None(self._add_mode, (SEND_MODE_NAMES[index], view_model.sendControlListView), lambda mixer: if len(mixer.sends) > self._send_offset + index:
pass1)

        for i in xrange(SEND_LIST_LENGTH):
            add_send_mode(i)
        

    
    def _add_mode(self, mode, view, parameter_getter, additional_mode_contents = []):
        description = MixerSectionDescription(view = view, parameter_getter = parameter_getter)
        self.add_mode(mode, additional_mode_contents + [
            partial(self._set_mode, description)])
        mode_button = self.get_mode_button(mode)
        mode_button.mode_selected_color = 'MixerControlView.SectionSelected'
        mode_button.mode_unselected_color = 'MixerControlView.SectionUnSelected'

    
    def on_enabled_changed(self):
        super(MixerControlComponent, self).on_enabled_changed()
        self._selected_view.visible = self.is_enabled()
        self._update_mixer_sections()
        if not self.is_enabled():
            self._update_realtime_ids()
        

    
    def set_mixer_section(self, mixer_section):
        self._mixer_section_view = mixer_section
        if self._mixer_section_view:
            self._mixer_section_view.model.mode = 'Global'
            self._update_mixer_sections()
        

    
    def number_sends(self):
        return len(self._track_provider.selected_item.mixer_device.sends)

    number_sends = property(number_sends)
    
    def _set_mode(self, description):
        self._selected_view.visible = False
        self._selected_view = description.view
        self._parameter_getter = description.parameter_getter
        self._update_controls(self._parameter_getter, self._selected_view)
        self._selected_view.visible = True

    
    def _on_mode_changed(self, selected_mode):
        if selected_mode in SEND_MODE_NAMES:
            index = SEND_MODE_NAMES.index(selected_mode)
            self._selected_item = SEND_SECTIONS[clamp(index + self._send_offset, 0, self.number_sends - 1)]
        elif selected_mode == 'panning':
            pass
        
        self._selected_item = MIXER_SECTIONS[0]
        self.notify_selected_item()

    _on_mode_changed = listens('selected_mode')(_on_mode_changed)
    
    def _on_return_tracks_changed(self):
        self._updating_send_offset_mode_selection().__enter__()
        
        try:
            self._update_mode_selection()
            new_send_offset = max(0, int(ceil(float(self.number_sends) / float(SEND_LIST_LENGTH) - 1) * SEND_LIST_LENGTH))
            if new_send_offset < self._send_offset:
                self._send_offset = new_send_offset
        finally:
            pass


    _on_return_tracks_changed = listens('return_tracks')(_on_return_tracks_changed)
    
    def _on_items_changed(self):
        self._update_controls(self._parameter_getter, self._selected_view)

    _on_items_changed = listens('items')(_on_items_changed)
    
    def _on_selected_item_changed(self):
        if self.number_sends <= SEND_LIST_LENGTH:
            self._send_offset = 0
        
        self._update_mode_selection()
        self._update_mixer_sections()
        self._update_buttons(self.selected_mode)

    _on_selected_item_changed = listens('selected_item')(_on_selected_item_changed)
    
    def _update_mode_selection(self):
        number_sends = self.number_sends
        if self.selected_mode in SEND_MODE_NAMES:
            index = SEND_MODE_NAMES.index(self.selected_mode)
            if index + self._send_offset >= number_sends and number_sends > 0:
                self.selected_mode = SEND_MODE_NAMES[number_sends % SEND_LIST_LENGTH - 1]
            elif index == 0 and number_sends == 0:
                self.selected_mode = 'panning'
            
        

    
    def _update_mixer_sections(self):
        if self.is_enabled():
            position = max(self._send_offset, 0)
            pos_range = min(self.number_sends - position, SEND_LIST_LENGTH)
            mixer_section_names = list(MIXER_SECTIONS) + SEND_SECTIONS[position:position + pos_range]
            continue
            self._mixer_sections = [ SimpleItemSlot(name = name) for name in mixer_section_names ]
            if self.number_sends > SEND_LIST_LENGTH:
                self._mixer_sections.extend([
                    SimpleItemSlot()] * (8 - len(self._mixer_sections)))
                self._mixer_sections[7] = SimpleItemSlot(icon = 'page_right.svg')
            
            self.notify_items()
            if self.selected_mode in SEND_MODE_NAMES:
                index = SEND_MODE_NAMES.index(self.selected_mode)
                self._selected_item = SEND_SECTIONS[index + self._send_offset]
                self.notify_selected_item()
            
        

    
    def items(self):
        return self._mixer_sections

    items = property(items)
    
    def selected_item(self):
        return self._selected_item

    selected_item = property(selected_item)
    
    def _update_controls(self, parameter_getter, control_view):
        parameters = self._get_parameter_for_tracks(parameter_getter)
        control_view.parameters = parameters
        self._update_realtime_ids()
        for (control, parameter) in map(None, self.controls, parameters):
            control.mapped_parameter = parameter
        

    
    def _update_realtime_ids(self):
        mixables = self._track_provider.items
        for (handler, mixable) in izip(self.real_time_meter_handlers, mixables):
            if liveobj_valid(mixable):
                pass
            1
            mixable.mixer_device(None)
        

    
    def _get_parameter_for_tracks(self, parameter_getter):
        tracks = self._track_provider.items
        self.controls.control_count = len(tracks)
        return (map,)(lambda t: if t:
pass1, tracks)

    
    def mode_can_be_used(self, mode):
        if not mode not in SEND_MODE_NAMES:
            pass
        return SEND_MODE_NAMES.index(mode) + self._send_offset < self.number_sends

    
    def _update_buttons(self, selected_mode):
        for name in self._mode_map.iterkeys():
            self.get_mode_button(name).enabled = self.mode_can_be_used(name)
        
        self.cycle_sends_button.enabled = self.number_sends > SEND_LIST_LENGTH

    
    def cycle_sends_button(self, button):
        button.color = 'MixerControlView.SectionSelected'

    cycle_sends_button = cycle_sends_button.pressed(cycle_sends_button)
    
    def cycle_sends_button(self, button):
        button.color = 'MixerControlView.SectionUnSelected'
        self._cycle_send_offset()

    cycle_sends_button = cycle_sends_button.released(cycle_sends_button)
    
    def _cycle_send_offset(self):
        self._updating_send_offset_mode_selection().__enter__()
        
        try:
            new_offset = self._send_offset + SEND_LIST_LENGTH
            if new_offset < self.number_sends:
                pass
            1
            self._send_offset = 0
            if self.selected_mode in SEND_MODE_NAMES:
                self.selected_mode = SEND_MODE_NAMES[0]
        finally:
            pass


    
    def _updating_send_offset_mode_selection(self):
        yield None
        self._update_mixer_sections()
        self._update_buttons(self.selected_mode)
        self._update_controls(self._parameter_getter, self._selected_view)

    _updating_send_offset_mode_selection = contextmanager(_updating_send_offset_mode_selection)

