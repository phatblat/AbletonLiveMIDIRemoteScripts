# Source Generated with Decompyle++
# File: automation.pyc (Python 2.5)

from __future__ import absolute_import
from itertools import ifilter
from ableton.v2.base import liveobj_valid, listenable_property
from pushbase.automation_component import AutomationComponent as AutomationComponentBase
from pushbase.parameter_provider import ParameterInfo
from internal_parameter import InternalParameterBase

class StepAutomationParameter(InternalParameterBase):
    
    def __init__(self, parameter = None, *a, **k):
        if not liveobj_valid(parameter):
            raise AssertionError
        super(StepAutomationParameter, self).__init__(name = parameter.name, *a, **a)
        self._parameter = parameter
        self._value = self._parameter.value

    
    def value(self):
        return self._value

    value = listenable_property(value)
    
    def value(self, value):
        self._value = value

    value = value.setter(value)
    
    def max(self):
        return self._parameter.max

    max = property(max)
    
    def min(self):
        return self._parameter.min

    min = property(min)
    
    def display_value(self):
        return self._parameter.str_for_value(self.value)

    display_value = property(display_value)
    
    def canonical_parent(self):
        return self._parameter.canonical_parent

    canonical_parent = property(canonical_parent)
    
    def original_parameter(self):
        return self._parameter

    original_parameter = property(original_parameter)
    
    def is_quantized(self):
        return self._parameter.is_quantized

    is_quantized = property(is_quantized)
    
    def value_items(self):
        return self._parameter.value_items

    value_items = property(value_items)
    
    def automation_state(self):
        return self._parameter.automation_state

    automation_state = property(automation_state)


def make_automation_parameter(parameter_info):
    wrapped_parameter = None
    if parameter_info and liveobj_valid(parameter_info.parameter):
        parameter = parameter_info.parameter
        wrapped_parameter = ParameterInfo(parameter = StepAutomationParameter(parameter = parameter), name = parameter_info.name, default_encoder_sensitivity = parameter_info.default_encoder_sensitivity, fine_grain_encoder_sensitivity = parameter_info.fine_grain_encoder_sensitivity)
    
    return wrapped_parameter


class AutomationComponent(AutomationComponentBase):
    ENCODER_SENSITIVITY_FACTOR = 0.5
    __events__ = ('parameters',)
    
    def __init__(self, *a, **k):
        self._parameter_infos = []
        super(AutomationComponent, self).__init__(*a, **a)
        self._drum_pad_selected = False

    
    def deviceType(self):
        device_type = 'default'
        if hasattr(self.parameter_provider, 'device'):
            device = self.parameter_provider.device()
            if liveobj_valid(device):
                pass
            1
            device_type = device_type
        
        return device_type

    deviceType = property(deviceType)
    
    def parameters(self):
        return map(lambda info: if info:
pass1, self._parameter_infos)

    parameters = property(parameters)
    
    def parameter_infos(self):
        return self._parameter_infos

    parameter_infos = property(parameter_infos)
    
    def set_drum_pad_selected(self, value):
        if self._drum_pad_selected != value:
            self._drum_pad_selected = value
            self.notify_can_automate_parameters()
        

    
    def can_automate_parameters(self):
        if self._can_automate_parameters():
            pass
        return not (self._drum_pad_selected)

    can_automate_parameters = listenable_property(can_automate_parameters)
    
    def update(self):
        super(AutomationComponent, self).update()
        if self.is_enabled():
            self._rebuild_parameter_list()
            self._update_parameter_values()
        

    
    def _update_parameters(self):
        self._rebuild_parameter_list()
        super(AutomationComponent, self)._update_parameters()

    
    def _rebuild_parameter_list(self):
        if self.is_enabled():
            self._parameter_infos = map(make_automation_parameter, self._parameter_infos_to_use())
        else:
            self._parameter_infos = []

    
    def _update_parameter_values(self):
        for info in ifilter(lambda p: p is not None, self._parameter_infos):
            if len(self._selected_time) > 0:
                wrapped_parameter = info.parameter
                wrapped_parameter.value = self.parameter_to_value(wrapped_parameter.original_parameter)
                continue
        
        self.notify_parameters()

    
    def _parameter_for_index(self, parameters, index):
        if parameters[index]:
            pass
        1


