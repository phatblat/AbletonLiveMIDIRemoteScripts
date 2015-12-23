# Source Generated with Decompyle++
# File: mixer_component.pyc (Python 2.5)

from itertools import izip
from ableton.v2.base import find_if, listenable_property, listens, listens_group, liveobj_valid, Subject, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent
from track_selection import get_all_mixer_tracks, mixable_button_color

class MixerDeviceMuteSoloComponent(Component):
    mute_button = ButtonControl()
    solo_button = ButtonControl()
    __events__ = ('mute_or_solo_pressed',)
    
    def __init__(self, *a, **k):
        super(MixerDeviceMuteSoloComponent, self).__init__(*a, **a)
        self.mute_button.enabled = False
        self.solo_button.enabled = False

    
    def set_track(self, track):
        self._track = track
        if self._track is not None:
            pass
        1
        enabled_state = False
        self.mute_button.enabled = enabled_state
        self.solo_button.enabled = enabled_state

    
    def track(self):
        return self._track

    track = property(track)
    
    def mute_button(self, button):
        self.toggle_mute()
        self.notify_mute_or_solo_pressed()

    mute_button = mute_button.pressed(mute_button)
    
    def toggle_mute(self):
        if self._track:
            self._track.mute = not (self._track.mute)
        

    
    def solo_button(self, button):
        self.toggle_solo()
        self.notify_mute_or_solo_pressed()

    solo_button = solo_button.pressed(solo_button)
    
    def toggle_solo(self):
        if self._track and self._track != self.song.master_track:
            song = self.song
            tracks = get_all_mixer_tracks(song)
            continue
            other_solos = _[1]([ track.solo for track in tracks ])
            if other_solos and song.exclusive_solo and not (self._track.solo):
                for track in tracks:
                    track.solo = False
                
            
            self._track.solo = not (self._track.solo)
        



class MixerButtonStateManager(Subject):
    is_pressed = listenable_property.managed(False)


class MixerComponent(MixerComponentBase, ModesComponent):
    solo_track_button = ButtonControl()
    mute_track_button = ButtonControl()
    MIXER_BUTTON_STATE_DELAY = 0.1
    
    def __init__(self, solo_layer = None, mute_layer = None, *a, **k):
        super(MixerComponent, self).__init__(*a, **a)
        self._allow_released_immediately_action = True
        self.mixer_button_state = self.register_disconnectable(MixerButtonStateManager())
        self._mixer_button_state_task = self._tasks.add(task.sequence(task.wait(self.MIXER_BUTTON_STATE_DELAY), task.run(self._update_mixer_button_state))).kill()
        self.add_mode('default', None)
        self.add_mode('solo', AddLayerMode(self, solo_layer))
        self.add_mode('mute', AddLayerMode(self, mute_layer))
        self.selected_mode = 'default'
        self._on_items_changed.subject = self._provider
        self._on_selected_item_changed.subject = self._provider
        self._on_selected_item_changed()
        self._update_channel_strip_button_colors()
        self._MixerComponent__on_channel_strip_mute_or_solo_changed.replace_subjects(self._channel_strips)

    
    def __on_channel_strip_mute_or_solo_changed(self, _):
        self._allow_released_immediately_action = False

    _MixerComponent__on_channel_strip_mute_or_solo_changed = listens_group('mute_or_solo_pressed')(__on_channel_strip_mute_or_solo_changed)
    
    def _create_strip(self):
        return MixerDeviceMuteSoloComponent()

    
    def _create_master_strip(self):
        return ChannelStripComponentBase()

    
    def _on_items_changed(self):
        mixer_tracks = self._provider.items
        for (track, channel_strip) in izip(mixer_tracks, self._channel_strips):
            channel_strip.set_track(track)
        
        self._on_solo_changed.replace_subjects(mixer_tracks)
        self._on_mute_changed.replace_subjects(mixer_tracks)
        self._update_button_state_colors()
        self._update_channel_strip_button_colors()

    _on_items_changed = listens('items')(_on_items_changed)
    
    def set_mute_buttons(self, buttons):
        for (strip, button) in map(None, self._channel_strips, []):
            strip.mute_button.set_control_element(button)

    
    def set_solo_buttons(self, buttons):
        for (strip, button) in map(None, self._channel_strips, []):
            strip.solo_button.set_control_element(button)

    
    def _reassign_tracks(self):
        self._on_items_changed()

    
    def _update_selected_strip(self):
        '''
        We are not interested in setting the selected channel strip, which occurs in the
        base mixer component.
        '''
        pass

    
    def _update_send_index(self):
        """
        We are not interested in the base mixer's send index, which is updated when the
        return tracks change. This also reassigns the send_controls, which we are not
        interested in doing.
        """
        pass

    
    def _mute_or_solo_is_pressed(self):
        if not self.solo_track_button.is_pressed:
            pass
        return self.mute_track_button.is_pressed

    
    def _update_mixer_button_state(self):
        self.mixer_button_state.is_pressed = self._mute_or_solo_is_pressed()

    
    def _on_selected_item_changed(self):
        self._update_button_state_colors()
        self._update_channel_strip_button_colors()

    _on_selected_item_changed = listens('selected_item')(_on_selected_item_changed)
    
    def _on_solo_changed(self, mixable):
        self._update_button_state_colors()
        self._update_channel_strip_button_colors()

    _on_solo_changed = listens_group('solo')(_on_solo_changed)
    
    def _on_mute_changed(self, mixable):
        self._update_button_state_colors()
        self._update_channel_strip_button_colors()

    _on_mute_changed = listens_group('mute')(_on_mute_changed)
    
    def solo_track_button(self, button):
        if self._allow_released_immediately_action:
            self._toggle_channel_strip_property(lambda channel_strip: channel_strip.toggle_solo())
        

    solo_track_button = solo_track_button.released_immediately(solo_track_button)
    
    def solo_track_button(self, button):
        self._allow_released_immediately_action = True
        self.push_mode('solo')
        self._mixer_button_state_task.restart()

    solo_track_button = solo_track_button.pressed(solo_track_button)
    
    def solo_track_button(self, button):
        self.pop_mode('solo')
        self.mixer_button_state.is_pressed = self._mute_or_solo_is_pressed()
        self._update_button_state_colors()

    solo_track_button = solo_track_button.released(solo_track_button)
    
    def mute_track_button(self, button):
        if self._allow_released_immediately_action:
            self._toggle_channel_strip_property(lambda channel_strip: channel_strip.toggle_mute())
        

    mute_track_button = mute_track_button.released_immediately(mute_track_button)
    
    def mute_track_button(self, button):
        self._allow_released_immediately_action = True
        self.push_mode('mute')
        self._mixer_button_state_task.restart()

    mute_track_button = mute_track_button.pressed(mute_track_button)
    
    def mute_track_button(self, button):
        self.pop_mode('mute')
        self.mixer_button_state.is_pressed = self._mute_or_solo_is_pressed()
        self._update_button_state_colors()

    mute_track_button = mute_track_button.released(mute_track_button)
    
    def _toggle_channel_strip_property(self, toggle_function):
        channel_strip = self._get_selected_track_channel_strip()
        if channel_strip:
            toggle_function(channel_strip)
        

    
    def _get_selected_track_channel_strip(self):
        selected_track = self._provider.selected_item
        return (find_if,)(lambda strip: strip.track == selected_track, self._channel_strips)

    
    def _update_channel_strip_button_colors(self):
        song = self.song
        for strip in self._channel_strips:
            color = mixable_button_color(strip.track, song, self._provider.selected_item)
            strip.mute_button.color = color
            strip.solo_button.color = color
        

    
    def _update_button_state_colors(self):
        song = self.song
        selected_track = self._provider.selected_item
        if selected_track != song.master_track:
            if liveobj_valid(selected_track):
                pass
            1
            self.mute_track_button.color = 'mute'(selected_track.mute, False, 'Mixer.MuteOff')
            if liveobj_valid(selected_track):
                pass
            1
            self.solo_track_button.color = 'solo'(selected_track.solo, False, 'Mixer.SoloOn')
        

    
    def _get_track_state_mode_state(self, mode, track_state_parameter, on_color):
        if track_state_parameter or self.selected_mode == mode:
            pass
        1
        return 'DefaultButton.On'


