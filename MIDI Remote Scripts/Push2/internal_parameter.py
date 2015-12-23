# Source Generated with Decompyle++
# File: internal_parameter.pyc (Python 2.5)

from __future__ import absolute_import
from Live import DeviceParameter
from ableton.v2.base import listenable_property, liveobj_valid, nop, Slot, SlotManager, Subject, SlotError

def identity(value, _parent):
    return value


def to_percentage_display(value):
    percentage = 100 * value
    percentage_str = '100'
    if percentage < 100:
        if percentage < 10:
            pass
        1
        precision = 1
        format_str = '%.' + str(precision) + 'f'
        percentage_str = format_str % percentage
    
    return unicode(percentage_str + ' %')


class InternalParameterBase(Subject):
    is_enabled = True
    is_quantized = False
    
    def __init__(self, name = None, *a, **k):
        if not name is not None:
            raise AssertionError
        super(InternalParameterBase, self).__init__(*a, **a)
        self._name = name

    
    def _has_valid_parent(self):
        return liveobj_valid(self._parent)

    
    def canonical_parent(self):
        raise NotImplementedError

    canonical_parent = property(canonical_parent)
    
    def display_value(self):
        raise NotImplementedError

    display_value = property(display_value)
    
    def min(self):
        raise NotImplementedError

    min = property(min)
    
    def max(self):
        raise NotImplementedError

    max = property(max)
    
    def value(self):
        raise NotImplementedError

    value = property(value)
    
    def name(self):
        return self._name

    name = property(name)
    
    def original_name(self):
        return self._name

    original_name = property(original_name)
    
    def default_value(self):
        return self.min

    default_value = property(default_value)
    
    def automation_state(self):
        return DeviceParameter.AutomationState.none

    automation_state = listenable_property(automation_state)
    
    def state(self):
        return DeviceParameter.ParameterState.enabled

    state = listenable_property(state)
    
    def _live_ptr(self):
        return id(self)

    _live_ptr = property(_live_ptr)
    
    def __str__(self):
        return self.display_value



class InternalParameter(InternalParameterBase):
    '''
    Class implementing the DeviceParameter interface. Using instances of this class,
    we can mix script-internal values with DeviceParameter instances.
    '''
    __events__ = ('value',)
    
    def __init__(self, parent = None, display_value_conversion = None, *a, **k):
        super(InternalParameter, self).__init__(*a, **a)
        self._value = 0
        self._parent = parent
        self.set_display_value_conversion(display_value_conversion)
        self.set_scaling_functions(None, None)

    
    def set_display_value_conversion(self, display_value_conversion):
        if not display_value_conversion:
            pass
        self._display_value_conversion = to_percentage_display
        self.notify_value()

    
    def set_scaling_functions(self, to_internal, from_internal):
        if not to_internal:
            pass
        self._to_internal = identity
        if not from_internal:
            pass
        self._from_internal = identity

    
    def canonical_parent(self):
        return self._parent

    canonical_parent = property(canonical_parent)
    
    def _get_value(self):
        if self._has_valid_parent():
            pass
        1
        return self.min

    
    def _set_value(self, new_value):
        if self.min <= new_value:
            pass
        new_value <= self.max
        if not 1:
            raise AssertionError, 'Invalid value %f' % new_value
        self.linear_value = self._to_internal(new_value, self._parent)

    value = property(_get_value, _set_value)
    
    def _get_linear_value(self):
        return self._value

    
    def _set_linear_value(self, new_value):
        if new_value != self._value:
            self._value = new_value
            self.notify_value()
        

    linear_value = property(_get_linear_value, _set_linear_value)
    
    def min(self):
        return 0

    min = property(min)
    
    def max(self):
        return 1

    max = property(max)
    
    def display_value(self):
        return self._display_value_conversion(self.value)

    display_value = property(display_value)


class WrappingParameter(InternalParameter, SlotManager):
    
    def __init__(self, source_property = None, from_property_value = None, to_property_value = None, display_value_conversion = nop, value_items = [], *a, **k):
        if not source_property is not None:
            raise AssertionError
        super(WrappingParameter, self).__init__(display_value_conversion = display_value_conversion, *a, **a)
        if not hasattr(self._parent, source_property) and source_property in dir(self._parent):
            raise AssertionError
        self._source_property = source_property
        self._value_items = value_items
        self.set_scaling_functions(to_property_value, from_property_value)
        self._property_slot = self.register_slot(Slot(listener = self.notify_value, event = source_property))
        self.connect()

    
    def connect(self):
        self._property_slot.subject = None
        self._property_slot.subject = self._parent

    
    def _get_property_value(self):
        if self._has_valid_parent():
            pass
        1
        return self.min

    
    def _get_value(self):
        
        try:
            if self._has_valid_parent():
                pass
            1
            return self.min
        except RuntimeError:
            return self.min


    
    def _set_value(self, new_value):
        if self.min <= new_value:
            pass
        new_value <= self.max
        if not 1:
            raise AssertionError, 'Invalid value %f' % new_value
        
        try:
            setattr(self._parent, self._source_property, self._to_internal(new_value, self._parent))
        except RuntimeError:
            pass


    linear_value = property(_get_value, _set_value)
    value = property(_get_value, _set_value)
    
    def display_value(self):
        
        try:
            value = self._get_property_value()
            return unicode(self._display_value_conversion(value))
        except RuntimeError:
            return unicode()


    display_value = property(display_value)
    
    def is_quantized(self):
        return len(self._value_items) > 0

    is_quantized = property(is_quantized)
    
    def value_items(self):
        return self._value_items

    value_items = property(value_items)


class EnumWrappingParameter(InternalParameterBase, SlotManager):
    is_enabled = True
    is_quantized = True
    
    def __init__(self, parent = None, values_property = None, index_property = None, value_type = int, to_index_conversion = None, from_index_conversion = None, *a, **k):
        if not parent is not None:
            raise AssertionError
        if not values_property is not None:
            raise AssertionError
        if not index_property is not None:
            raise AssertionError
        super(EnumWrappingParameter, self).__init__(*a, **a)
        self._parent = parent
        self._values_property = values_property
        self._index_property = index_property
        if not to_index_conversion:
            pass
        
        self._to_index = lambda x: x
        if not from_index_conversion:
            pass
        
        self._from_index = lambda x: x
        self.value_type = value_type
        self._index_property_slot = self.register_slot(self._parent, self.notify_value, index_property)
        
        try:
            self.register_slot(self._parent, self.notify_value_items, values_property)
        except SlotError:
            pass


    
    def connect(self):
        self._index_property_slot.subject = None
        self._index_property_slot.subject = self._parent

    
    def display_value(self):
        index = self._get_index()
        values = self._get_values()
        if index < len(values):
            return unicode(values[index])
        else:
            return unicode()

    display_value = property(display_value)
    
    def value_items(self):
        return self._get_values()

    value_items = listenable_property(value_items)
    
    def value(self):
        return self._get_index()

    value = listenable_property(value)
    
    def value(self, new_value):
        self._set_index(new_value)

    value = value.setter(value)
    
    def _get_values(self):
        if self._has_valid_parent():
            pass
        1
        return []

    
    def _get_index(self):
        if self._has_valid_parent():
            pass
        1
        return int(getattr(self._parent, self._index_property))(0)

    
    def _set_index(self, index):
        index = self._to_index(index)
        setattr(self._parent, self._index_property, self.value_type(index))

    
    def canonical_parent(self):
        pass

    canonical_parent = property(canonical_parent)
    
    def max(self):
        return len(self.value_items) - 1

    max = property(max)
    
    def min(self):
        return 0

    min = property(min)


class RelativeInternalParameter(InternalParameter):
    __events__ = ('delta',)
    
    def default_value(self):
        return 0.5

    default_value = property(default_value)
    
    def _get_value(self):
        return self.default_value

    
    def _set_value(self, new_value):
        delta = new_value - self.value
        if delta != 0:
            self.notify_value()
            self.notify_delta(delta)
        

    value = property(_get_value, _set_value)
    linear_value = property(_get_value, _set_value)

