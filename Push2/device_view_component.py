# Source Generated with Decompyle++
# File: device_view_component.pyc (Python 2.5)

from ableton.v2.base import const, listens, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.mode import ModesComponent

class DeviceViewConnector(Component):
    
    def __init__(self, parameter_provider = None, device_type_provider = const('default'), view = None, *a, **k):
        if not parameter_provider is not None:
            raise AssertionError
        if not view is not None:
            raise AssertionError
        super(DeviceViewConnector, self).__init__(*a, **a)
        self._parameter_provider = parameter_provider
        self._view = view
        self._parameters = None
        self._device_type_provider = device_type_provider

    
    def update(self):
        super(DeviceViewConnector, self).update()
        if self.is_enabled():
            self._view.deviceType = self._device_type_provider()
        
        parameters = self._value_for_state(map(lambda p: if p:
passp.parameter, self._parameter_provider.parameters), [])
        if parameters != self._parameters:
            self._view.parameters = parameters
            self._parameters = parameters
        

    
    def on_enabled_changed(self):
        self._view.visible = self.is_enabled()
        self._on_parameters_changed.subject = self._value_for_state(self._parameter_provider, None)
        super(DeviceViewConnector, self).on_enabled_changed()

    
    def _on_parameters_changed(self):
        self.update()

    _on_parameters_changed = listens('parameters')(_on_parameters_changed)
    
    def _value_for_state(self, enabled_value, disabled_value):
        if self.is_enabled():
            pass
        1
        return disabled_value



class SimplerDeviceViewConnector(DeviceViewConnector):
    
    def __init__(self, device_component = None, *a, **k):
        super(SimplerDeviceViewConnector, self).__init__(*a, **a)
        self._device = device_component
        self._SimplerDeviceViewConnector__on_processed_zoom_requests_changed.subject = device_component

    
    def update(self):
        super(SimplerDeviceViewConnector, self).update()
        device = self._value_for_state(self._device.device(), None)
        if not device == None and device.class_name == 'OriginalSimpler':
            raise AssertionError
        self._view.properties = device
        self._view.wants_waveform_shown = self._parameter_provider.wants_waveform_shown
        self._view.simpler = device
        self._update_zoom_requests()

    
    def _update_zoom_requests(self):
        self._view.processed_zoom_requests = self._parameter_provider.processed_zoom_requests

    
    def __on_processed_zoom_requests_changed(self):
        self._update_zoom_requests()

    _SimplerDeviceViewConnector__on_processed_zoom_requests_changed = listens('processed_zoom_requests')(__on_processed_zoom_requests_changed)


class DeviceViewComponent(ModesComponent):
    
    def __init__(self, device_component = None, view_model = None, *a, **k):
        if not device_component is not None:
            raise AssertionError
        if not view_model is not None:
            raise AssertionError
        super(DeviceViewComponent, self).__init__(*a, **a)
        self._get_device = device_component.device
        for view in (view_model.deviceParameterView, view_model.simplerDeviceView):
            view.visible = False
        
        self.add_mode('default', DeviceViewConnector(parameter_provider = device_component, device_type_provider = self._device_type, view = view_model.deviceParameterView, is_enabled = False))
        self.add_mode('OriginalSimpler', SimplerDeviceViewConnector(parameter_provider = device_component, device_component = device_component, device_type_provider = self._device_type, view = view_model.simplerDeviceView, is_enabled = False))
        self.selected_mode = 'default'
        self._on_parameters_changed.subject = device_component

    
    def _device_type(self):
        device = self._get_device()
        if liveobj_valid(device):
            pass
        1
        return ''

    
    def _mode_to_select(self):
        device = self._get_device()
        if device:
            pass
        device_type = device.class_name
        if self.get_mode(device_type) != None:
            pass
        1
        return 'default'

    
    def _on_parameters_changed(self):
        self.selected_mode = self._mode_to_select()

    _on_parameters_changed = listens('parameters')(_on_parameters_changed)

