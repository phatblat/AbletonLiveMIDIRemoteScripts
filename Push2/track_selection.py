# Source Generated with Decompyle++
# File: track_selection.pyc (Python 2.5)

from functools import partial
from itertools import chain, ifilter, izip
import Live
from ableton.v2.base import SlotManager, Subject, const, depends, flatten, nop, listenable_property, listens, listens_group, liveobj_changed, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import SessionRingComponent, right_align_return_tracks_track_assigner
from ableton.v2.control_surface.control import ButtonControl, control_list
from ableton.v2.control_surface.components.view_control import has_next_item, next_item, TrackScroller as TrackScrollerBase, ViewControlComponent as ViewControlComponentBase
from pushbase.device_chain_utils import find_instrument_devices
from pushbase.actions import is_clip_stop_pending
from pushbase.consts import MessageBoxText
from pushbase.message_box_component import Messenger
from pushbase.special_chan_strip_component import toggle_arm
from colors import translate_color_index
from decoration import TrackDecoratorFactory
from item_lister_component import ItemProvider
from mixable_utilities import can_play_clips, is_chain
from observable_property_alias import ObservablePropertyAlias
from stop_clip_component import track_color_with_pending_stop
DeviceType = Live.Device.DeviceType

def mixable_button_color(mixer_track, song, selected_track = None):
    color = 'Mixer.NoTrack'
    if mixer_track:
        if can_play_clips(mixer_track) and is_clip_stop_pending(mixer_track):
            color = track_color_with_pending_stop(mixer_track)
        elif mixer_track.solo:
            color = 'Mixer.SoloOn'
        elif mixer_track == selected_track and not (mixer_track.mute):
            color = 'Mixer.TrackSelected'
        elif mixer_track.mute or mixer_track.muted_via_solo:
            color = 'Mixer.MutedTrack'
        else:
            color = translate_color_index(mixer_track.color_index)
    
    return color


class SelectedMixerTrackProvider(Subject, SlotManager):
    
    def __init__(self, song = None, *a, **k):
        super(SelectedMixerTrackProvider, self).__init__(*a, **a)
        self._view = song.view
        self._selected_mixer_track = None
        self._on_selected_track_changed.subject = self._view
        self._on_selected_chain_changed.subject = self._view
        self._on_selected_track_changed()

    __init__ = depends(song = None)(__init__)
    
    def _on_selected_track_changed(self):
        self._on_selected_mixer_track_changed()

    _on_selected_track_changed = listens('selected_track')(_on_selected_track_changed)
    
    def _on_selected_chain_changed(self):
        self._on_selected_mixer_track_changed()

    _on_selected_chain_changed = listens('selected_chain')(_on_selected_chain_changed)
    
    def selected_mixer_track(self):
        return self._get_selected_chain_or_track()

    selected_mixer_track = listenable_property(selected_mixer_track)
    
    def selected_mixer_track(self, track_or_chain):
        unwrapped_track = getattr(track_or_chain, 'proxied_object', track_or_chain)
        if liveobj_changed(self._selected_mixer_track, unwrapped_track):
            if isinstance(unwrapped_track, Live.Chain.Chain):
                self._view.selected_chain = unwrapped_track
                instruments = list(find_instrument_devices(self._view.selected_track))
                if instruments:
                    instruments[0].view.selected_chain = unwrapped_track
                
            else:
                self._view.selected_track = unwrapped_track
        

    selected_mixer_track = selected_mixer_track.setter(selected_mixer_track)
    
    def _on_selected_mixer_track_changed(self):
        selected_mixer_track = self._get_selected_chain_or_track()
        if liveobj_changed(self._selected_mixer_track, selected_mixer_track):
            self._selected_mixer_track = selected_mixer_track
            self.notify_selected_mixer_track(self.selected_mixer_track)
        

    
    def _get_selected_chain_or_track(self):
        selected_chain = self._view.selected_chain
        if selected_chain:
            pass
        1
        return self._view.selected_track



def get_flattened_track(track):
    '''
    Returns a flat list of a track with its instrument chains (when visible), or just the
    original track
    '''
    flat_track = [
        track]
    if track.can_show_chains and track.is_showing_chains:
        instruments = list(find_instrument_devices(track))
        continue
        _[1]([ c for c in instruments[0].chains ])
    
    return flat_track


def get_all_mixer_tracks(song):
    tracks = []
    for track in song.visible_tracks:
        tracks.extend(get_flattened_track(track))
    
    return tracks + list(song.return_tracks)


class SessionRingTrackProvider(SessionRingComponent, ItemProvider):
    
    def __init__(self, set_session_highlight = nop, *a, **k):
        self._decorator_factory = TrackDecoratorFactory()
        super(SessionRingTrackProvider, self).__init__(set_session_highlight = partial(set_session_highlight, include_rack_chains = True), *a, **a)
        self._artificially_selected_item = None
        self._on_tracklist_changed.subject = self.song
        self._update_listeners()
        self._selected_track = self.register_disconnectable(SelectedMixerTrackProvider())
        self._on_selected_item_changed.subject = self._selected_track

    __init__ = depends(set_session_highlight = const(nop))(__init__)
    
    def scroll_into_view(self, mixable):
        mixable_index = self.tracks_to_use().index(mixable)
        new_offset = self.track_offset
        if mixable_index >= self.track_offset + self.num_tracks:
            new_offset = (mixable_index - self.num_tracks) + 1
        elif mixable_index < self.track_offset:
            new_offset = mixable_index
        
        self.track_offset = new_offset

    
    def _get_selected_item(self):
        track_or_chain = self._selected_track.selected_mixer_track
        if liveobj_valid(self._artificially_selected_item):
            track_or_chain = self._artificially_selected_item
        
        return self._decorator_factory.decorated_objects.get(track_or_chain, track_or_chain)

    
    def _set_selected_item(self, item):
        self._artificially_selected_item = None
        self._selected_track.selected_mixer_track = item
        self.notify_selected_item()

    selected_item = property(_get_selected_item, _set_selected_item)
    
    def items(self):
        return right_align_return_tracks_track_assigner(self._song, self)

    items = property(items)
    
    def move(self, tracks, scenes):
        super(SessionRingTrackProvider, self).move(tracks, scenes)
        self._on_tracklist_changed()

    
    def tracks_to_use(self):
        return self._decorator_factory.decorate_all_mixer_tracks(get_all_mixer_tracks(self.song))

    
    def controlled_tracks(self):
        continue
        return [ getattr(track, 'proxied_object', track) for track in self.items ]

    
    def set_selected_item_without_updating_view(self, item):
        self._artificially_selected_item = item
        self.notify_selected_item()

    
    def synchronize_selection_with_live_view(self):
        '''
        Makes sure the currently selected item is also selected in Live.
        '''
        if self._artificially_selected_item:
            self.selected_item = self._artificially_selected_item
        

    
    def _on_tracklist_changed(self):
        self._notify_and_update()

    _on_tracklist_changed = listens('visible_tracks')(_on_tracklist_changed)
    
    def _on_is_showing_chains_changed(self, _):
        self._notify_and_update()

    _on_is_showing_chains_changed = listens_group('is_showing_chains')(_on_is_showing_chains_changed)
    
    def _on_chains_changed(self, _):
        if not self.song.view.selected_track.can_show_chains:
            self.selected_item = self.song.view.selected_track
        
        self._notify_and_update()

    _on_chains_changed = listens_group('chains')(_on_chains_changed)
    
    def _on_devices_changed(self, _):
        self._notify_and_update()

    _on_devices_changed = listens_group('devices')(_on_devices_changed)
    
    def _notify_and_update(self):
        self._ensure_valid_track_offset()
        self.notify_items()
        self.notify_tracks()
        self._update_listeners()

    
    def _update_listeners(self):
        
        def flattened_list_of_instruments(instruments):
            return list(flatten(instruments))

        tracks = self.song.tracks
        self._on_devices_changed.replace_subjects(tracks)
        continue
        chain_listenable_tracks = _[1]
        continue
        instruments = [](_[2])
        self._on_is_showing_chains_changed.replace_subjects(chain_listenable_tracks)
        self._on_chains_changed.replace_subjects(instruments)
        self._on_instrument_return_chains_changed.replace_subjects(instruments)

    
    def _ensure_valid_track_offset(self):
        max_index = len(self.tracks_to_use()) - 1
        clamped_offset = min(self.track_offset, max_index)
        if clamped_offset != self.track_offset:
            self.track_offset = clamped_offset
        

    
    def _on_instrument_return_chains_changed(self, _):
        self._notify_and_update()

    _on_instrument_return_chains_changed = listens_group('return_chains')(_on_instrument_return_chains_changed)
    
    def _on_selected_item_changed(self, _):
        self.notify_selected_item()

    _on_selected_item_changed = listens('selected_mixer_track')(_on_selected_item_changed)


def number_of_solos(song):
    continue
    return [](_[1])


class MixerTrackListComponent(Component, Messenger):
    select_buttons = control_list(ButtonControl, control_count = 8)
    delete_buttons = control_list(ButtonControl, control_count = 8)
    duplicate_buttons = control_list(ButtonControl, control_count = 8)
    arm_buttons = control_list(ButtonControl, control_count = 8)
    
    def __init__(self, tracks_provider = None, trigger_recording_on_release_callback = nop, *a, **k):
        if not tracks_provider is not None:
            raise AssertionError
        super(MixerTrackListComponent, self).__init__(*a, **a)
        self._can_trigger_recording_callback = trigger_recording_on_release_callback
        self._track_provider = tracks_provider
        self._selected_track = self.register_disconnectable(SelectedMixerTrackProvider())
        self._MixerTrackListComponent__on_items_changed.subject = self._track_provider
        self._MixerTrackListComponent__on_selected_item_changed.subject = self._track_provider
        self._MixerTrackListComponent__on_tracks_changed.subject = self.song
        self._MixerTrackListComponent__on_selected_track_changed.subject = self.song.view
        self._update_track_and_chain_listeners()
        self._update_button_enabled_state()
        self._update_all_button_colors()

    
    def tracks(self):
        return self._track_provider.items

    tracks = listenable_property(tracks)
    
    def selected_track(self):
        return self._track_provider.selected_item

    selected_track = listenable_property(selected_track)
    
    def absolute_selected_track_index(self):
        song = self.song
        tracks = song.tracks + song.return_tracks + (song.master_track,)
        selected_track = song.view.selected_track
        return list(tracks).index(selected_track)

    absolute_selected_track_index = listenable_property(absolute_selected_track_index)
    
    def __on_tracks_changed(self):
        self._update_track_and_chain_listeners()
        self._update_button_enabled_state()

    _MixerTrackListComponent__on_tracks_changed = listens('tracks')(__on_tracks_changed)
    
    def __on_track_mute_state_changed(self, track):
        self._update_all_button_colors()

    _MixerTrackListComponent__on_track_mute_state_changed = listens_group('mute')(__on_track_mute_state_changed)
    
    def __on_track_solo_state_changed(self, track):
        self._update_all_button_colors()

    _MixerTrackListComponent__on_track_solo_state_changed = listens_group('solo')(__on_track_solo_state_changed)
    
    def __on_track_fired_slot_changed(self, track):
        self._update_all_button_colors()

    _MixerTrackListComponent__on_track_fired_slot_changed = listens_group('fired_slot_index')(__on_track_fired_slot_changed)
    
    def __on_items_changed(self):
        self._update_track_and_chain_listeners()
        self._update_button_enabled_state()

    _MixerTrackListComponent__on_items_changed = listens('items')(__on_items_changed)
    
    def _update_track_and_chain_listeners(self):
        self.notify_tracks()
        self._MixerTrackListComponent__on_track_color_index_changed.replace_subjects(self.tracks)
        tracks_without_chains = ifilter(can_play_clips, self.tracks)
        self._MixerTrackListComponent__on_track_fired_slot_changed.replace_subjects(tracks_without_chains)
        continue
        all_tracks = [ _ for _ in chain(self.song.tracks, self.tracks) ]
        self._MixerTrackListComponent__on_track_mute_state_changed.replace_subjects(all_tracks)
        self._MixerTrackListComponent__on_track_solo_state_changed.replace_subjects(all_tracks)
        self._MixerTrackListComponent__on_track_muted_via_solo_changed.replace_subjects(all_tracks)
        self._update_button_enabled_state()
        self._update_all_button_colors()

    
    def _update_button_enabled_state(self):
        tracks = self.tracks
        for (track, control) in chain(izip(tracks, self.select_buttons), izip(tracks, self.delete_buttons), izip(tracks, self.arm_buttons), izip(tracks, self.duplicate_buttons)):
            control.enabled = liveobj_valid(track)
        

    
    def __on_track_color_index_changed(self, _):
        self._update_all_button_colors()

    _MixerTrackListComponent__on_track_color_index_changed = listens_group('color_index')(__on_track_color_index_changed)
    
    def __on_selected_item_changed(self):
        self.notify_selected_track()
        self._update_all_button_colors()

    _MixerTrackListComponent__on_selected_item_changed = listens('selected_item')(__on_selected_item_changed)
    
    def __on_selected_track_changed(self):
        self.notify_absolute_selected_track_index()

    _MixerTrackListComponent__on_selected_track_changed = listens('selected_track')(__on_selected_track_changed)
    
    def __on_track_muted_via_solo_changed(self, mixable):
        self._update_all_button_colors()

    _MixerTrackListComponent__on_track_muted_via_solo_changed = listens_group('muted_via_solo')(__on_track_muted_via_solo_changed)
    
    def _update_all_button_colors(self):
        for (index, mixer_track) in enumerate(self.tracks):
            color = mixable_button_color(mixer_track, self.song, self.selected_track)
            self.select_buttons[index].color = color
            self.duplicate_buttons[index].color = color
            self.delete_buttons[index].color = color
            self.arm_buttons[index].color = color
        

    
    def select_buttons(self, button):
        track = self.tracks[button.index]
        if track:
            if self._track_provider.selected_item != track:
                self._track_provider.selected_item = track
            elif hasattr(track, 'is_foldable') and track.is_foldable:
                track.fold_state = not (track.fold_state)
            
            if hasattr(track, 'is_showing_chains') and track.can_show_chains:
                track.is_showing_chains = not (track.is_showing_chains)
            
        

    select_buttons = select_buttons.pressed(select_buttons)
    
    def can_duplicate_or_delete(track_or_chain, return_tracks):
        unwrapped = track_or_chain.proxied_object
        if isinstance(unwrapped, Live.Track.Track):
            pass
        return unwrapped not in list(return_tracks)

    can_duplicate_or_delete = staticmethod(can_duplicate_or_delete)
    
    def delete_buttons(self, button):
        track_or_chain = self.tracks[button.index]
        if self.can_duplicate_or_delete(track_or_chain, self.song.return_tracks):
            
            try:
                track_index = list(self.song.tracks).index(track_or_chain)
                name = track_or_chain.name
                self.song.delete_track(track_index)
                self.show_notification(MessageBoxText.DELETE_TRACK % name)
            except RuntimeError:
                self.show_notification(MessageBoxText.TRACK_DELETE_FAILED)
            


    delete_buttons = delete_buttons.pressed(delete_buttons)
    
    def duplicate_buttons(self, button):
        track_or_chain = self.tracks[button.index]
        if self.can_duplicate_or_delete(track_or_chain, self.song.return_tracks):
            
            try:
                track_index = list(self.song.tracks).index(track_or_chain)
                self.song.duplicate_track(track_index)
                self.show_notification(MessageBoxText.DUPLICATE_TRACK % track_or_chain.name)
                self._update_all_button_colors()
            except Live.Base.LimitationError:
                self.show_notification(MessageBoxText.TRACK_LIMIT_REACHED)
            except RuntimeError:
                self.show_notification(MessageBoxText.TRACK_DUPLICATION_FAILED)
            


    duplicate_buttons = duplicate_buttons.pressed(duplicate_buttons)
    
    def arm_buttons(self, button):
        track_or_chain = self.tracks[button.index]
        if not is_chain(track_or_chain) and track_or_chain.can_be_armed:
            song = self.song
            toggle_arm(track_or_chain, song, exclusive = song.exclusive_arm)
        
        self._can_trigger_recording_callback(False)

    arm_buttons = arm_buttons.pressed(arm_buttons)


class TrackScroller(TrackScrollerBase, Subject):
    __events__ = ('scrolled',)
    
    def __init__(self, tracks_provider = None, *a, **k):
        if not tracks_provider is not None:
            raise AssertionError
        super(TrackScroller, self).__init__(*a, **a)
        self._track_provider = tracks_provider

    __init__ = depends(tracks_provider = None)(__init__)
    
    def _all_items(self):
        return self._track_provider.tracks_to_use() + [
            self._song.master_track]

    
    def _do_scroll(self, delta):
        track = next_item(self._all_items(), self._track_provider.selected_item, delta)
        self._track_provider.selected_item = track
        if isinstance(track, Live.Track.Track):
            self._select_scene_of_playing_clip(track)
        
        self.notify_scrolled()

    
    def _can_scroll(self, delta):
        
        try:
            return has_next_item(self._all_items(), self._track_provider.selected_item, delta)
        except ValueError:
            return False




class ViewControlComponent(ViewControlComponentBase):
    __events__ = ('selection_changed',)
    
    def __init__(self, tracks_provider = None, *a, **k):
        self._track_provider = tracks_provider
        super(ViewControlComponent, self).__init__(*a, **a)
        self._on_items_changed.subject = self._track_provider
        self._on_selected_item_changed.subject = self._track_provider

    __init__ = depends(tracks_provider = None)(__init__)
    
    def _create_track_scroller(self):
        scroller = TrackScroller(tracks_provider = self._track_provider)
        self.register_disconnectable(ObservablePropertyAlias(self, property_host = scroller, property_name = 'scrolled', alias_name = 'selection_changed'))
        return scroller

    
    def _on_items_changed(self):
        self._update_track_scroller()

    _on_items_changed = listens('items')(_on_items_changed)
    
    def _on_selected_item_changed(self):
        self._update_track_scroller()

    _on_selected_item_changed = listens('selected_item')(_on_selected_item_changed)
    
    def _update_track_scroller(self):
        self._scroll_tracks.update()


