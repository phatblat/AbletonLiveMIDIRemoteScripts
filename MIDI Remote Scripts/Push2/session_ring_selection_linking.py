# Source Generated with Decompyle++
# File: session_ring_selection_linking.pyc (Python 2.5)

from ableton.v2.base.slot import SlotManager, listens
from ableton.v2.base.dependency import depends
from ableton.v2.base.util import index_if

class SessionRingSelectionLinking(SlotManager):
    
    def __init__(self, session_ring = None, selection_changed_notifier = None, song = None, *a, **k):
        super(SessionRingSelectionLinking, self).__init__(*a, **a)
        if not session_ring is not None:
            raise AssertionError
        if not selection_changed_notifier is not None:
            raise AssertionError
        if not song is not None:
            raise AssertionError
        self._session_ring = session_ring
        self._song = song
        self._on_selection_changed.subject = selection_changed_notifier

    __init__ = depends(song = None)(__init__)
    
    def _on_selection_changed(self):
        if self._song.view.selected_track == self._song.master_track:
            return None
        
        track_index = self._current_track_index()
        right_ring_index = self._session_ring.track_offset + self._session_ring.num_tracks - 1
        offset_left = track_index - self._session_ring.track_offset
        offset_right = track_index - right_ring_index
        adjustment = min(0, offset_left) + max(0, offset_right)
        new_track_offset = self._session_ring.track_offset + adjustment
        if new_track_offset != self._session_ring.track_offset:
            self._session_ring.set_offsets(new_track_offset, self._session_ring.scene_offset)
        

    _on_selection_changed = listens('selection_changed')(_on_selection_changed)
    
    def _current_track_index(self):
        current_track = self._session_ring.selected_item
        return (index_if,)(lambda t: t == current_track, self._session_ring.tracks_to_use())


