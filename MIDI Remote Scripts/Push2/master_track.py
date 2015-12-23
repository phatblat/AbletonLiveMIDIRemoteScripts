# Source Generated with Decompyle++
# File: master_track.pyc (Python 2.5)

from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ToggleButtonControl

class MasterTrackComponent(Component):
    toggle_button = ToggleButtonControl()
    
    def __init__(self, tracks_provider = None, *a, **k):
        if not tracks_provider is not None:
            raise AssertionError
        super(MasterTrackComponent, self).__init__(*a, **a)
        self._tracks_provider = tracks_provider
        self._MasterTrackComponent__on_selected_item_changed.subject = self._tracks_provider
        self._previous_selection = self._tracks_provider.selected_item
        self._update_button_state()

    
    def __on_selected_item_changed(self, *a):
        self._update_button_state()
        if not self._is_on_master():
            self._previous_selection = self._tracks_provider.selected_item
        

    _MasterTrackComponent__on_selected_item_changed = listens('selected_item')(__on_selected_item_changed)
    
    def _update_button_state(self):
        self.toggle_button.is_toggled = self._is_on_master()

    
    def toggle_button(self, toggled, button):
        if toggled:
            self._previous_selection = self._tracks_provider.selected_item
            self._tracks_provider.selected_item = self.song.master_track
        else:
            self._tracks_provider.selected_item = self._previous_selection
        self._update_button_state()

    toggle_button = toggle_button.toggled(toggle_button)
    
    def _is_on_master(self):
        return self._tracks_provider.selected_item == self.song.master_track


