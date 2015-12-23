# Source Generated with Decompyle++
# File: stop_clip_component.pyc (Python 2.5)

from itertools import count
from ableton.v2.base import listens_group
from ableton.v2.control_surface.control import ButtonControl
from pushbase.actions import is_clip_stop_pending, StopClipComponent as StopClipComponentBase
from colors import make_blinking_track_color, make_pulsing_track_color
from skin_default import RECORDING_COLOR, UNLIT_COLOR

def track_color_with_pending_stop(track):
    return make_blinking_track_color(track, UNLIT_COLOR)


class StopClipComponent(StopClipComponentBase):
    stop_selected_track_clip_button = ButtonControl()
    
    def stop_selected_track_clip_button(self, button):
        self._stop_clip_in_selected_track()

    stop_selected_track_clip_button = stop_selected_track_clip_button.released_immediately(stop_selected_track_clip_button)
    
    def _stop_clip_in_selected_track(self):
        song = self.song
        selected_track = song.view.selected_track
        if selected_track != song.master_track and selected_track not in song.return_tracks:
            selected_track.stop_all_clips()
        

    
    def _assign_listeners(self, tracks):
        super(StopClipComponent, self)._assign_listeners(tracks)
        self._StopClipComponent__on_mute_changed.replace_subjects(tracks, count())
        self._StopClipComponent__on_solo_changed.replace_subjects(tracks, count())

    
    def __on_mute_changed(self, track_index):
        self._update_stop_button_by_index(track_index)

    _StopClipComponent__on_mute_changed = listens_group('mute')(__on_mute_changed)
    
    def __on_solo_changed(self, track_index):
        self._update_stop_button_by_index(track_index)

    _StopClipComponent__on_solo_changed = listens_group('solo')(__on_solo_changed)
    
    def _color_for_button(self, track):
        if is_clip_stop_pending(track):
            return track_color_with_pending_stop(track)
        elif track.playing_slot_index >= 0:
            if track.solo:
                return 'StopClips.SoloedTrack'
            elif track.mute:
                return 'StopClips.MutedTrack'
            elif track.clip_slots[track.playing_slot_index].is_recording:
                pulse_to = RECORDING_COLOR
            else:
                pulse_to = UNLIT_COLOR
            return make_pulsing_track_color(track, pulse_to)
        else:
            return super(StopClipComponent, self)._color_for_button(track)


