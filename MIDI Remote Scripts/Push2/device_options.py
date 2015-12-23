# Source Generated with Decompyle++
# File: device_options.pyc (Python 2.5)

from __future__ import absolute_import
from ableton.v2.base import liveobj_valid, listenable_property, listens, const, Subject, Slot, SlotManager

class DeviceTriggerOption(Subject):
    __events__ = ('default_label',)
    
    def __init__(self, name = None, default_label = None, callback = None, is_active = None):
        if not callback:
            raise AssertionError
        self.trigger = callback
        if not name:
            pass
        self._name = 'Option'
        if not default_label:
            pass
        self._default_label = self._name
        if not is_active:
            pass
        self._is_active_callback = const(True)

    
    def name(self):
        return self._name

    name = property(name)
    
    def active(self):
        return self._is_active()

    active = listenable_property(active)
    
    def _is_active(self):
        return self._is_active_callback()

    
    def _get_default_label(self):
        return self._default_label

    
    def _set_default_label(self, label):
        self._default_label = label
        self.notify_default_label()

    default_label = property(_get_default_label, _set_default_label)


class DeviceSwitchOption(SlotManager, DeviceTriggerOption):
    
    def __init__(self, second_label = None, parameter = None, *a, **k):
        super(DeviceSwitchOption, self).__init__(callback = self.cycle_index, *a, **a)
        if not second_label:
            pass
        self._second_label = ''
        self.set_parameter(parameter)

    
    def set_parameter(self, parameter):
        self._parameter = parameter
        self._DeviceSwitchOption__on_value_changed.subject = parameter
        self.notify_active_index()
        self.notify_active()

    
    def _is_active(self):
        if super(DeviceSwitchOption, self)._is_active():
            pass
        return liveobj_valid(self._parameter)

    
    def active_index(self):
        if liveobj_valid(self._parameter):
            pass
        1
        return 0

    active_index = listenable_property(active_index)
    
    def __on_value_changed(self):
        self.notify_active_index()

    _DeviceSwitchOption__on_value_changed = listens('value')(__on_value_changed)
    
    def second_label(self):
        return self._second_label

    second_label = property(second_label)
    
    def cycle_index(self):
        if liveobj_valid(self._parameter):
            self._parameter.value = float((self.active_index + 1) % 2)
        



class DeviceOnOffOption(SlotManager, DeviceTriggerOption):
    ON_LABEL = 'ON'
    OFF_LABEL = 'OFF'
    
    def __init__(self, name = None, property_host = None, property_name = '', *a, **k):
        super(DeviceOnOffOption, self).__init__(callback = self.cycle_index, name = name, *a, **a)
        self._property_host = property_host
        self._property_name = property_name
        
        def notify_index_and_default_label():
            self.notify_active_index()
            self.notify_default_label()

        self._property_slot = self.register_slot(Slot(subject = property_host, event = property_name, listener = notify_index_and_default_label))

    
    def _property_value(self):
        if liveobj_valid(self._property_host):
            pass
        1
        return False

    
    def _is_active(self):
        if super(DeviceOnOffOption, self)._is_active():
            pass
        return liveobj_valid(self._property_host)

    
    def active_index(self):
        return int(not self._property_value())

    active_index = listenable_property(active_index)
    
    def cycle_index(self):
        if liveobj_valid(self._property_host):
            value_type = type(self._property_value())
            new_value = not bool((self.active_index + 1) % 2)
            setattr(self._property_host, self._property_name, value_type(new_value))
        

    
    def default_label(self):
        if self._property_value():
            pass
        1
        return self._default_label % (self.ON_LABEL, self.OFF_LABEL)

    default_label = property(default_label)

