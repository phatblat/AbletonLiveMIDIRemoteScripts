# Source Generated with Decompyle++
# File: simpler_zoom.pyc (Python 2.5)

from __future__ import absolute_import, with_statement
from contextlib import contextmanager
from ableton.v2.base import clamp, linear, SlotManager, Subject, listens, liveobj_valid, liveobj_changed

def is_simpler(device):
    if device:
        pass
    return device.class_name == 'OriginalSimpler'


def get_zoom_parameter(parameter_host):
    if liveobj_valid(parameter_host):
        pass
    1
    parameters = []
    results = filter(lambda p: p.name == 'Zoom', parameters)
    if len(results) > 0:
        pass
    1


class ZoomHandling(SlotManager, Subject):
    __events__ = ('zoom',)
    SCREEN_WIDTH = 960
    ZOOM_EXP = 10
    DEFAULT_ZOOM_START_FUDGE = 0.2
    _parameter_host = None
    _zoom_parameter = None
    
    def zoom(self):
        if self._zoom_parameter:
            pass
        1
        return 0

    zoom = property(zoom)
    
    def max_zoom(self):
        return NotImplementedError

    max_zoom = property(max_zoom)
    
    def zoom_factor(self):
        factor = 1
        if self.zoom > 0:
            minimum = 1
            factor = 1 / linear(minimum, self.max_zoom, self.zoom)
        
        return factor

    zoom_factor = property(zoom_factor)
    
    def _on_zoom_changed(self):
        self.notify_zoom()

    _on_zoom_changed = listens('value')(_on_zoom_changed)
    
    def _get_zoom_start_fudge(self):
        ''' Return fudge for lowest zoom value, assuming ZOOM_EXP == 10.0.

        _internal_to_zoom and _zoom_to_internal adjust for some mysterious
        behaviour elsewhere with a fudge to map the lowest non-zero internal
        value to a higher zoom value, determined by the return value of this
        funtion.

        The sensible return value of this depends on the exponent of the curve
        used in those functions. To account for the fact that ZOOM_EXP is
        can be changed in subclasses or in the future, this function should return
        a value which assumes a ZOOM_EXP of 10.0.
        '''
        return self.DEFAULT_ZOOM_START_FUDGE

    
    def _internal_to_zoom(self, value, _parent):
        fudge = self._get_zoom_start_fudge() ** 10 ** (1 / self.ZOOM_EXP)
        if value > 0:
            pass
        1
        return 0

    
    def _zoom_to_internal(self, value, _parent):
        fudge = self._get_zoom_start_fudge() ** 10 ** (1 / self.ZOOM_EXP)
        linear_value = (value ** (1 / self.ZOOM_EXP) - fudge) / (1 - fudge)
        return clamp(linear_value, 0, 1)

    
    def request_zoom(self, factor):
        if self._zoom_parameter:
            self._zoom_parameter.value = factor
        

    
    def _set_zoom_parameter(self):
        return NotImplementedError

    
    def set_parameter_host(self):
        return NotImplementedError



class SimplerZoomHandling(ZoomHandling):
    
    def __init__(self):
        ZoomHandling.__init__(self)
        self.ZOOM_EXP = 20

    
    def set_parameter_host(self, parameter_host):
        if is_simpler(parameter_host):
            pass
        1
        new_parameter_host = None
        if liveobj_changed(self._parameter_host, new_parameter_host):
            old_zoom = self.zoom
            self._parameter_host = new_parameter_host
            self._updating_zoom_scaling().__enter__()
            
            try:
                self._set_zoom_parameter()
            finally:
                pass

            self._on_zoom_changed.subject = self._zoom_parameter
            self._on_sample_changed.subject = self._parameter_host
            if self.zoom != old_zoom:
                self.notify_zoom()
            
        

    
    def _set_zoom_parameter(self):
        self._zoom_parameter = get_zoom_parameter(self._parameter_host)

    
    def _on_sample_changed(self):
        if self._zoom_parameter:
            self._zoom_parameter.value = self._zoom_parameter.default_value
        

    _on_sample_changed = listens('sample_file_path')(_on_sample_changed)
    
    def _updating_zoom_scaling(self):
        if self._zoom_parameter:
            self._zoom_parameter.set_scaling_functions(None, None)
        
        yield None
        if self._zoom_parameter:
            self._zoom_parameter.set_scaling_functions(self._zoom_to_internal, self._internal_to_zoom)
        

    _updating_zoom_scaling = contextmanager(_updating_zoom_scaling)
    
    def max_zoom(self):
        if liveobj_valid(self._parameter_host):
            pass
        has_sample = self._parameter_host.sample_length > 0
        if has_sample:
            pass
        1
        length = self._parameter_host.sample_length(self.SCREEN_WIDTH)
        return float(length / self.SCREEN_WIDTH)

    max_zoom = property(max_zoom)
    
    def _get_zoom_start_fudge(self):
        if liveobj_valid(self._parameter_host):
            sample_length = self._parameter_host.sample_length
            fudge_length_a = 200000
            fudge_factor_a = 0.4
            fudge_length_b = 2500000
            fudge_factor_b = 0.2
            if sample_length < fudge_length_a:
                return fudge_factor_a
            
            if sample_length > fudge_length_b:
                return fudge_factor_b
            
            return ((sample_length - fudge_length_a) / (fudge_length_b - fudge_length_a)) * (fudge_factor_b - fudge_factor_a) + fudge_factor_a
        else:
            return self.DEFAULT_ZOOM_START_FUDGE


