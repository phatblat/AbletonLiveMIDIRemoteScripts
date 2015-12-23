# Source Generated with Decompyle++
# File: convert.pyc (Python 2.5)

from functools import partial
from itertools import izip
import Live
from ableton.v2.base import find_if, listenable_property, listens, listens_group, liveobj_valid, SlotManager, Subject, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl, control_list
from pushbase.device_chain_utils import find_instrument_devices
from colors import UNCOLORED_INDEX
from decoration import find_decorated_object
from device_decoration import SimplerDecoratedPropertiesCopier
from drum_group_component import find_all_simplers_on_pad, find_simplers
from mixable_utilities import find_drum_rack_instrument, find_simpler, is_audio_track, is_midi_track
from track_selection import SelectedMixerTrackProvider

def possible_conversions(track, decorator_factory = None):
    conversions = []
    if liveobj_valid(track):
        if is_midi_track(track) and len(track.devices) > 0:
            drum_rack = find_drum_rack_instrument(track)
            if liveobj_valid(drum_rack):
                drum_pad = drum_rack.view.selected_drum_pad
                if liveobj_valid(drum_pad) and len(drum_pad.chains) == 1 and find_instrument_devices(drum_pad.chains[0]):
                    conversions.append(DrumPadToMidiTrack(drum_pad = drum_pad, track = track))
                
            else:
                simpler = find_simpler(track)
                if simpler != None and simpler.playback_mode == Live.SimplerDevice.PlaybackMode.slicing:
                    conversions.append(SlicesToDrumRack(device = simpler, track = track))
                else:
                    conversions.append(MoveDeviceChain(device = simpler, track = track, decorator_factory = decorator_factory))
        elif is_audio_track(track):
            highlighted_clip_slot = track.canonical_parent.view.highlighted_clip_slot
            clip = (find_if,)(lambda slot: if slot.has_clip:
passhighlighted_clip_slot == slot, track.clip_slots)
            if liveobj_valid(clip) and not (clip.is_recording):
                conversions.append(CreateTrackWithSimpler(clip_slot = highlighted_clip_slot, track = track))
            
        
    
    return conversions


class ConvertAction(Subject, SlotManager):
    __events__ = ('action_invalidated',)
    needs_deferred_invocation = False
    color_source = None
    name_source = None
    
    def __init__(self, color_source = None, name_source = None, *a, **k):
        super(ConvertAction, self).__init__(*a, **a)
        self.color_source = color_source
        self.name_source = name_source

    
    def convert(self, song):
        raise NotImplementedError



class TrackBasedConvertAction(ConvertAction):
    
    def __init__(self, track = None, *a, **k):
        if not liveobj_valid(track):
            raise AssertionError
        super(TrackBasedConvertAction, self).__init__(color_source = track, name_source = track, *a, **a)
        self._track = track



class MoveDeviceChain(TrackBasedConvertAction):
    name = 'Drum Pad'
    
    def __init__(self, device = None, decorator_factory = None, *a, **k):
        super(MoveDeviceChain, self).__init__(*a, **a)
        self._decorator_factory = decorator_factory
        if hasattr(device, 'playback_mode'):
            self._MoveDeviceChain__on_playback_mode_changed.subject = device
        

    
    def convert(self, song):
        self._track.stop_all_clips()
        track_index = list(song.tracks).index(self._track)
        copiers = self._create_copiers()
        drum_pad = Live.Conversions.move_devices_on_track_to_new_drum_rack_pad(song, track_index)
        if liveobj_valid(drum_pad) and copiers:
            self._apply_simpler_properties(drum_pad, song, copiers)
        

    
    def __on_playback_mode_changed(self):
        self.notify_action_invalidated()

    _MoveDeviceChain__on_playback_mode_changed = listens('playback_mode')(__on_playback_mode_changed)
    
    def _apply_simpler_properties(self, drum_pad, song, copiers):
        destination_simplers = find_all_simplers_on_pad(drum_pad)
        for (copier, destination) in izip(copiers, destination_simplers):
            if copier:
                copier.apply_properties(destination, song)
                continue
        

    
    def _create_copiers(self):
        
        def create_copier_if_decorated(simpler):
            decorated = find_decorated_object(simpler, self._decorator_factory)
            if decorated:
                pass
            1

        return map(create_copier_if_decorated, find_simplers(self._track))



class CreateTrackWithSimpler(ConvertAction):
    name = 'Simpler'
    
    def __init__(self, clip_slot = None, track = None, *a, **k):
        if not liveobj_valid(clip_slot):
            raise AssertionError
        if not liveobj_valid(track):
            raise AssertionError
        super(CreateTrackWithSimpler, self).__init__(name_source = clip_slot.clip, color_source = clip_slot.clip, *a, **a)
        self._clip_slot = clip_slot
        self._track = track
        self._CreateTrackWithSimpler__on_has_clip_changed.subject = self._clip_slot

    
    def convert(self, song):
        self._track.stop_all_clips()
        Live.Conversions.create_midi_track_with_simpler(song, self._clip_slot.clip)

    
    def __on_has_clip_changed(self):
        self.notify_action_invalidated()

    _CreateTrackWithSimpler__on_has_clip_changed = listens('has_clip')(__on_has_clip_changed)


class SlicesToDrumRack(TrackBasedConvertAction):
    needs_deferred_invocation = True
    name = 'Drum Rack'
    
    def __init__(self, device = None, *a, **k):
        if not isinstance(device, Live.SimplerDevice.SimplerDevice):
            raise AssertionError
        super(SlicesToDrumRack, self).__init__(*a, **a)
        self._device = device
        self._SlicesToDrumRack__on_playback_mode_changed.subject = self._device
        self._SlicesToDrumRack__on_sample_file_path_changed.subject = self._device

    
    def convert(self, song):
        Live.Conversions.sliced_simpler_to_drum_rack(song, self._device)

    
    def __on_playback_mode_changed(self):
        self.notify_action_invalidated()

    _SlicesToDrumRack__on_playback_mode_changed = listens('playback_mode')(__on_playback_mode_changed)
    
    def __on_sample_file_path_changed(self):
        self.notify_action_invalidated()

    _SlicesToDrumRack__on_sample_file_path_changed = listens('sample_file_path')(__on_sample_file_path_changed)


class DrumPadToMidiTrack(ConvertAction):
    name = 'MIDI track'
    
    def __init__(self, drum_pad = None, track = None, *a, **k):
        if not liveobj_valid(drum_pad):
            raise AssertionError
        super(DrumPadToMidiTrack, self).__init__(name_source = drum_pad, color_source = track, *a, **a)
        self._DrumPadToMidiTrack__on_devices_changed.subject = drum_pad.chains[0]
        self._DrumPadToMidiTrack__on_chains_changed.subject = drum_pad
        self._drum_pad = drum_pad

    
    def __on_devices_changed(self):
        self.notify_action_invalidated()

    _DrumPadToMidiTrack__on_devices_changed = listens('devices')(__on_devices_changed)
    
    def __on_chains_changed(self):
        self.notify_action_invalidated()

    _DrumPadToMidiTrack__on_chains_changed = listens('chains')(__on_chains_changed)
    
    def convert(self, song):
        Live.Conversions.create_midi_track_from_drum_pad(song, self._drum_pad)



class ConvertComponent(Component):
    __events__ = ('cancel',)
    action_buttons = control_list(ButtonControl, color = 'Option.Unselected', pressed_color = 'Option.Selected')
    cancel_button = ButtonControl(color = 'Option.Unselected', pressed_color = 'Option.Selected')
    source_color_index = listenable_property.managed(UNCOLORED_INDEX)
    source_name = listenable_property.managed(unicode(''))
    
    def __init__(self, tracks_provider = None, conversions_provider = possible_conversions, decorator_factory = None, *a, **k):
        if not tracks_provider is not None:
            raise AssertionError
        if not callable(conversions_provider):
            raise AssertionError
        super(ConvertComponent, self).__init__(*a, **a)
        self._tracks_provider = tracks_provider
        self._conversions_provider = conversions_provider
        self._decorator_factory = decorator_factory
        self._available_conversions = []
        self._update_possible_conversions()

    
    def available_conversions(self):
        return map(lambda x: x.name, self._available_conversions)

    available_conversions = listenable_property(available_conversions)
    
    def on_enabled_changed(self):
        super(ConvertComponent, self).on_enabled_changed()
        self._update_possible_conversions()

    
    def _update_possible_conversions(self):
        for conversion in self._available_conversions:
            self.disconnect_disconnectable(conversion)
        
        track = self._tracks_provider.selected_item
        self._available_conversions = map(self.register_disconnectable, self._conversions_provider(track, self._decorator_factory))
        self._ConvertComponent__on_action_invalidated.replace_subjects(self._available_conversions)
        color_sources = map(lambda c: c.color_source, self._available_conversions)
        name_sources = map(lambda c: c.name_source, self._available_conversions)
        self._ConvertComponent__on_action_source_color_index_changed.replace_subjects(color_sources)
        self._ConvertComponent__on_action_source_name_changed.replace_subjects(name_sources)
        if self._available_conversions:
            first_action = self._available_conversions[0]
            self._ConvertComponent__on_action_source_color_index_changed(first_action.color_source)
            self._ConvertComponent__on_action_source_name_changed(first_action.name_source)
        
        self.action_buttons.control_count = len(self._available_conversions)
        self.notify_available_conversions()

    
    def __on_action_source_color_index_changed(self, color_source):
        if color_source and color_source.color_index is not None:
            pass
        1
        self.source_color_index = UNCOLORED_INDEX

    _ConvertComponent__on_action_source_color_index_changed = listens_group('color_index')(__on_action_source_color_index_changed)
    
    def __on_action_source_name_changed(self, name_source):
        if name_source:
            pass
        1
        self.source_name = unicode()

    _ConvertComponent__on_action_source_name_changed = listens_group('name')(__on_action_source_name_changed)
    
    def action_buttons(self, button):
        if self._do_conversion(button.index):
            self.notify_cancel()
        

    action_buttons = action_buttons.released(action_buttons)
    
    def _do_conversion(self, action_index):
        self._update_possible_conversions()
        if action_index < len(self._available_conversions):
            action = self._available_conversions[action_index]
            if action.needs_deferred_invocation:
                None(self._tasks.add(task.sequence, (task.delay(1), task.run)(lambda : self._do_conversion_deferred(action))))
                return False
            else:
                self._invoke_conversion(action)
        
        return True

    
    def _do_conversion_deferred(self, action):
        self._invoke_conversion(action)
        self.notify_cancel()

    
    def _invoke_conversion(self, action):
        action.convert(self.song)

    
    def cancel_button(self, button):
        self.notify_cancel()

    cancel_button = cancel_button.released(cancel_button)
    
    def __on_action_invalidated(self, action):
        self.notify_cancel()

    _ConvertComponent__on_action_invalidated = listens_group('action_invalidated')(__on_action_invalidated)


class ConvertEnabler(Component):
    convert_toggle_button = ButtonControl(color = 'DefaultButton.On')
    
    def __init__(self, enter_dialog_mode = None, exit_dialog_mode = None, *a, **k):
        if not enter_dialog_mode is not None:
            raise AssertionError
        if not exit_dialog_mode is not None:
            raise AssertionError
        super(ConvertEnabler, self).__init__(*a, **a)
        self._enter_dialog_mode = partial(enter_dialog_mode, 'convert')
        self._exit_dialog_mode = partial(exit_dialog_mode, 'convert')
        self._selected_item = self.register_disconnectable(SelectedMixerTrackProvider(song = self.song))
        self._ConvertEnabler__on_selected_item_changed.subject = self._selected_item
        self._ConvertEnabler__on_selected_item_changed(None)
        song = self.song
        self._ConvertEnabler__on_devices_changed.subject = song.view
        self._ConvertEnabler__on_selected_scene_changed.subject = song.view
        self._update_clip_slot_listener()
        self._update_drum_pad_listeners()

    
    def __on_selected_item_changed(self, _):
        self._update_clip_slot_listener()
        self._disable_and_check_enabled_state()

    _ConvertEnabler__on_selected_item_changed = listens('selected_mixer_track')(__on_selected_item_changed)
    
    def convert_toggle_button(self, button):
        self._enter_dialog_mode()

    convert_toggle_button = convert_toggle_button.pressed(convert_toggle_button)
    
    def _can_enable_mode(self):
        conversions = possible_conversions(self._selected_item.selected_mixer_track)
        has_conversions = bool(conversions)
        for conversion in conversions:
            conversion.disconnect()
        
        return has_conversions

    
    def _disable_and_check_enabled_state(self):
        self._exit_dialog_mode()
        self.convert_toggle_button.enabled = self._can_enable_mode()

    
    def __on_devices_changed(self):
        self._disable_and_check_enabled_state()
        self._update_drum_pad_listeners()

    _ConvertEnabler__on_devices_changed = listens('selected_track.devices')(__on_devices_changed)
    
    def _update_drum_pad_listeners(self):
        drum_rack = find_drum_rack_instrument(self._selected_item.selected_mixer_track)
        if liveobj_valid(drum_rack):
            pass
        1
        drum_rack_view_or_none = None
        self._ConvertEnabler__on_selected_drum_pad_changed.subject = drum_rack_view_or_none
        self._ConvertEnabler__on_drum_pad_chains_changed.subject = drum_rack_view_or_none

    
    def __on_selected_drum_pad_changed(self):
        self._disable_and_check_enabled_state()
        drum_rack_view = self._ConvertEnabler__on_selected_drum_pad_changed.subject
        if liveobj_valid(drum_rack_view):
            selected_drum_pad = drum_rack_view.selected_drum_pad
            first_chain_or_none = None
            if liveobj_valid(selected_drum_pad):
                if len(selected_drum_pad.chains) > 0:
                    pass
                1
                first_chain_or_none = None
            
            self._ConvertEnabler__on_drum_pad_chain_devices_changed.subject = first_chain_or_none
        

    _ConvertEnabler__on_selected_drum_pad_changed = listens('selected_drum_pad')(__on_selected_drum_pad_changed)
    
    def __on_drum_pad_chains_changed(self):
        self._disable_and_check_enabled_state()

    _ConvertEnabler__on_drum_pad_chains_changed = listens('selected_drum_pad.chains')(__on_drum_pad_chains_changed)
    
    def __on_drum_pad_chain_devices_changed(self):
        self._disable_and_check_enabled_state()

    _ConvertEnabler__on_drum_pad_chain_devices_changed = listens('devices')(__on_drum_pad_chain_devices_changed)
    
    def __on_selected_scene_changed(self):
        self._update_clip_slot_listener()
        self._disable_and_check_enabled_state()

    _ConvertEnabler__on_selected_scene_changed = listens('selected_scene')(__on_selected_scene_changed)
    
    def _update_clip_slot_listener(self):
        clip_slot = self.song.view.highlighted_clip_slot
        self._ConvertEnabler__on_clip_slot_has_clip_changed.subject = clip_slot

    
    def __on_clip_slot_has_clip_changed(self):
        self._disable_and_check_enabled_state()
        clip_slot = self._ConvertEnabler__on_clip_slot_has_clip_changed.subject
        self._update_clip_listeners(clip_slot)

    _ConvertEnabler__on_clip_slot_has_clip_changed = listens('has_clip')(__on_clip_slot_has_clip_changed)
    
    def _update_clip_listeners(self, clip_slot):
        self._ConvertEnabler__on_clip_playing_status_changed.subject = clip_slot.clip
        self._ConvertEnabler__on_clip_recording_status_changed.subject = clip_slot.clip

    
    def __on_clip_recording_status_changed(self):
        self._disable_and_check_enabled_state()

    _ConvertEnabler__on_clip_recording_status_changed = listens('is_recording')(__on_clip_recording_status_changed)
    
    def __on_clip_playing_status_changed(self):
        self._disable_and_check_enabled_state()

    _ConvertEnabler__on_clip_playing_status_changed = listens('playing_status')(__on_clip_playing_status_changed)

