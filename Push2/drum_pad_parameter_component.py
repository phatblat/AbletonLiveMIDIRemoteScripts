# Source Generated with Decompyle++
# File: drum_pad_parameter_component.pyc (Python 2.5)

from __future__ import absolute_import
from ableton.v2.base import clamp, listenable_property, listens, liveobj_valid, SlotManager
from ableton.v2.control_surface import CompoundComponent
from ableton.v2.control_surface.control import StepEncoderControl
from pushbase.parameter_provider import generate_info, ParameterProvider
from device_view_component import DeviceViewConnector
from internal_parameter import InternalParameterBase
NO_CHOKE_GROUP = u'None'
MAX_CHOKE_GROUP = 16
NUM_CHOKE_GROUPS = MAX_CHOKE_GROUP + 1

class ChokeParameter(SlotManager, InternalParameterBase):
    is_quantized = True
    value_items = [
        NO_CHOKE_GROUP] + map(unicode, range(1, NUM_CHOKE_GROUPS))
    min = 0
    max = MAX_CHOKE_GROUP
    
    def __init__(self, drum_pad = None, *a, **k):
        if not liveobj_valid(drum_pad):
            raise AssertionError
        super(ChokeParameter, self).__init__(name = 'Choke', *a, **a)
        self._pad = drum_pad
        self._on_pad_updated.subject = drum_pad

    
    def _on_pad_updated(self):
        self.notify_value()

    _on_pad_updated = listens('choke_group')(_on_pad_updated)
    
    def value(self):
        if len(self._pad.chains) > 0:
            pass
        1
        return 0

    value = listenable_property(value)
    
    def value(self, value):
        value = clamp(value, 0, MAX_CHOKE_GROUP)
        self._pad.choke_group = value

    value = value.setter(value)
    
    def canonical_parent(self):
        return self._pad

    canonical_parent = property(canonical_parent)
    
    def display_value(self):
        return unicode(self.value)

    display_value = property(display_value)


def parameters_for_pad(pad):
    if not pad or len(pad.chains) == 0:
        return []
    
    return [
        generate_info(ChokeParameter(drum_pad = pad))]


class DrumPadParameterComponent(CompoundComponent, ParameterProvider):
    choke_encoder = StepEncoderControl(num_steps = 10)
    
    def __init__(self, view_model = None, *a, **k):
        if not view_model is not None:
            raise AssertionError
        super(DrumPadParameterComponent, self).__init__(*a, **a)
        self._drum_pad = None
        self._parameters = []
        self._view_connector = self.register_component(DeviceViewConnector(parameter_provider = self, view = view_model.deviceParameterView))

    
    def _get_drum_pad(self):
        return self._drum_pad

    
    def _set_drum_pad(self, pad):
        if pad != self._drum_pad:
            self._drum_pad = pad
            self._rebuild_parameter_list()
            self._on_chains_in_pad_changed.subject = self._drum_pad
        

    drum_pad = property(_get_drum_pad, _set_drum_pad)
    
    def _on_chains_in_pad_changed(self):
        self._rebuild_parameter_list()

    _on_chains_in_pad_changed = listens('chains')(_on_chains_in_pad_changed)
    
    def _rebuild_parameter_list(self):
        for info in self._parameters:
            self.disconnect_disconnectable(info.parameter)
        
        self._parameters = parameters_for_pad(self._drum_pad)
        for info in self._parameters:
            self.register_disconnectable(info.parameter)
        
        self._view_connector.update()

    
    def parameters(self):
        return self._parameters

    parameters = property(parameters)
    
    def choke_encoder(self, value, encoder):
        if len(self._parameters) > 0:
            self._parameters[0].parameter.value += value
        

    choke_encoder = choke_encoder.value(choke_encoder)

