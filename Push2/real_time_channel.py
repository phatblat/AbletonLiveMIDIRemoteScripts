# Source Generated with Decompyle++
# File: real_time_channel.pyc (Python 2.5)

from ableton.v2.control_surface import Component
from ableton.v2.base import depends, listenable_property, liveobj_changed, liveobj_valid

class RealTimeDataComponent(Component):
    
    def __init__(self, real_time_mapper = None, register_real_time_data = None, channel_type = None, *a, **k):
        if not channel_type is not None:
            raise AssertionError
        if not liveobj_valid(real_time_mapper):
            raise AssertionError
        super(RealTimeDataComponent, self).__init__(*a, **a)
        self._channel_type = channel_type
        self._real_time_channel_id = ''
        self._object_id = ''
        self._real_time_mapper = real_time_mapper
        self._data = None
        self._valid = True
        register_real_time_data(self)

    __init__ = depends(real_time_mapper = None, register_real_time_data = None)(__init__)
    
    def channel_id(self):
        return self._real_time_channel_id

    channel_id = listenable_property(channel_id)
    
    def object_id(self):
        return self._object_id

    object_id = listenable_property(object_id)
    
    def on_enabled_changed(self):
        super(RealTimeDataComponent, self).on_enabled_changed()
        self.invalidate()
        self.update_attachment()

    
    def set_data(self, data):
        if liveobj_changed(data, self._data):
            self._data = data
            self.invalidate()
        

    
    def invalidate(self):
        self._valid = False

    
    def update_attachment(self):
        if not self._valid:
            if self._real_time_channel_id != '':
                self._real_time_mapper.detach_channel(self._real_time_channel_id)
                self._real_time_channel_id = ''
            
            if self.is_enabled():
                pass
            1
            data = None
            if data != None:
                (self._real_time_channel_id, self._object_id) = self._real_time_mapper.attach_object(data, self._channel_type)
            
            self.notify_channel_id()
            self.notify_object_id()
            self._valid = True
        


