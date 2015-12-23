# Source Generated with Decompyle++
# File: simpler_slice_nudging.pyc (Python 2.5)

from __future__ import absolute_import, with_statement
from contextlib import contextmanager
import Live
from ableton.v2.base import SlotManager, find_if, liveobj_valid, clamp, listens
from simpler_zoom import is_simpler
CENTERED_NUDGE_VALUE = 0.5
MINIMUM_SLICE_DISTANCE = 2

class SimplerSliceNudging(SlotManager):
    _simpler = None
    _nudge_parameter = None
    
    def set_device(self, device):
        if is_simpler(device):
            pass
        1
        self._simpler = None
        self._SimplerSliceNudging__on_selected_slice_changed.subject = self._simpler
        self._updating_nudge_parameter().__enter__()
        
        try:
            if liveobj_valid(self._simpler):
                pass
            1
            self._nudge_parameter = lambda p: p.name == 'Nudge'(self._simpler.parameters, [])
        finally:
            pass


    
    def _updating_nudge_parameter(self):
        if self._nudge_parameter:
            self._nudge_parameter.set_display_value_conversion(None)
        
        yield None
        if self._nudge_parameter:
            self._nudge_parameter.set_display_value_conversion(self._display_value_conversion)
        
        self._SimplerSliceNudging__on_nudge_delta.subject = self._nudge_parameter

    _updating_nudge_parameter = contextmanager(_updating_nudge_parameter)
    
    def _can_access_slicing_properties(self):
        if liveobj_valid(self._simpler) and self._simpler.current_playback_mode == str(Live.SimplerDevice.PlaybackMode.slicing):
            pass
        return self._simpler.sample_length > 0

    
    def __on_selected_slice_changed(self):
        if self._nudge_parameter:
            self._nudge_parameter.notify_value()
        

    _SimplerSliceNudging__on_selected_slice_changed = listens('view.selected_slice')(__on_selected_slice_changed)
    
    def __on_nudge_delta(self, delta):
        if self._can_access_slicing_properties():
            old_slice_time = self._simpler.view.selected_slice
            if old_slice_time >= 0:
                if self._is_first_slice_at_time(old_slice_time):
                    new_start = self._new_start_marker_time(old_slice_time, delta)
                    self._simpler.start_marker = new_start
                    return None
                
                new_slice_time = self._new_slice_time(old_slice_time, delta)
                if old_slice_time != new_slice_time:
                    original_slices = self._simpler.slices
                    self._simpler.insert_slice(new_slice_time)
                    self._simpler.remove_slice(old_slice_time)
                    
                    try:
                        self._simpler.view.selected_slice = new_slice_time
                    except RuntimeError:
                        self._simpler.view.selected_slice = self._simpler.slices[list(original_slices).index(old_slice_time)]
                    

            
        

    _SimplerSliceNudging__on_nudge_delta = listens('delta')(__on_nudge_delta)
    
    def _is_first_slice_at_time(self, slice_time):
        start_sample = self._simpler.start_marker
        return abs(slice_time - start_sample) < MINIMUM_SLICE_DISTANCE

    
    def _new_start_marker_time(self, old_slice_time, delta):
        change_in_samples = self._sample_change_from_delta(delta)
        new_start_marker_time = old_slice_time + change_in_samples
        return clamp(new_start_marker_time, 0, self._simpler.sample_length - MINIMUM_SLICE_DISTANCE)

    
    def _sample_change_from_delta(self, delta):
        sample_length = self._simpler.sample_length
        change_in_samples = round(delta * sample_length / 10)
        return int(change_in_samples)

    
    def _get_surrounding_slices(self, slice_time):
        slices = list(self._simpler.slices)
        index = slices.index(slice_time)
        sample_length = self._simpler.sample_length
        if index > 0:
            pass
        1
        previous_slice = 0
        if index < len(slices) - 1:
            pass
        1
        next_slice = sample_length
        return (previous_slice, next_slice)

    
    def _display_value_conversion(self, _value):
        if self._can_access_slicing_properties():
            pass
        1
        selected_slice = -1
        if selected_slice >= 0:
            pass
        1
        return '-'

    
    def _get_min_first_slice_length(self):
        return Live.SimplerDevice.get_min_first_slice_length_in_samples(self._simpler.proxied_object)

    
    def _new_slice_time(self, old_slice_time, delta):
        (previous_slice, next_slice) = self._get_surrounding_slices(old_slice_time)
        change_in_samples = self._sample_change_from_delta(delta)
        min_second_slice_start = self._simpler.start_marker + self._get_min_first_slice_length()
        lower_bound = max(0, min_second_slice_start, previous_slice)
        upper_bound = min(next_slice, self._simpler.end_marker, self._simpler.sample_length) - MINIMUM_SLICE_DISTANCE
        return clamp(old_slice_time + change_in_samples, lower_bound, upper_bound)


