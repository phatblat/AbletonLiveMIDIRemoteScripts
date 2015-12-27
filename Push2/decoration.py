# Source Generated with Decompyle++
# File: decoration.pyc (Python 2.5)

from __future__ import absolute_import
from itertools import ifilter
import Live
from ableton.v2.base import CompoundDisconnectable, find_if, liveobj_changed, liveobj_valid, Proxy

def find_decorated_object(proxied_object, decorator_factory):
    decorated_obj = None
    if liveobj_valid(proxied_object):
        decorated_obj = (find_if,)(lambda obj: not liveobj_changed(obj.proxied_object, proxied_object), decorator_factory.decorated_objects.itervalues())
    
    return decorated_obj


class LiveObjectDecorator(CompoundDisconnectable, Proxy):
    
    def __init__(self, live_object = None, additional_properties = { }):
        if not live_object is not None:
            raise AssertionError
        super(LiveObjectDecorator, self).__init__(proxied_object = live_object)
        self._live_object = live_object
        for (name, value) in additional_properties.iteritems():
            setattr(self, name, value)
        

    
    def __eq__(self, other):
        if not id(self) == id(other):
            pass
        return self._live_object == other

    
    def __ne__(self, other):
        return not (self == other)

    
    def __nonzero__(self):
        return self._live_object != None

    
    def __hash__(self):
        return hash(self._live_object)



class LiveObjectDict(dict):
    
    def __init__(self, *a, **k):
        self.update(*a, **a)

    
    def __getitem__(self, key):
        return super(LiveObjectDict, self).__getitem__(self._transform_key(key))

    
    def __setitem__(self, key, value):
        return super(LiveObjectDict, self).__setitem__(self._transform_key(key), value)

    
    def __delitem__(self, key):
        return super(LiveObjectDict, self).__delitem__(self._transform_key(key))

    
    def __contains__(self, key):
        return super(LiveObjectDict, self).__contains__(self._transform_key(key))

    
    def get(self, key, *default):
        return super(LiveObjectDict, self).get(self._transform_key(key), *default)

    
    def _transform_key(self, key):
        if not hasattr(key, '_live_ptr'):
            raise AssertionError
        return key._live_ptr

    
    def update(self, *a, **k):
        trans = self._transform_key
        continue
        [](*_[1], **_[1])

    
    def prune(self, keys):
        transformed_keys = map(self._transform_key, keys)
        deleted_objects = []
        for key in (ifilter,)(lambda x: x not in transformed_keys, self.keys()):
            deleted_objects.append(super(LiveObjectDict, self).__getitem__(key))
            super(LiveObjectDict, self).__delitem__(key)
        
        return deleted_objects



class DecoratorFactory(CompoundDisconnectable):
    _decorator = LiveObjectDecorator
    
    def __init__(self, *a, **k):
        super(DecoratorFactory, self).__init__(*a, **a)
        self.decorated_objects = LiveObjectDict()

    
    def decorate(self, live_object, additional_properties = { }, **k):
        if self._should_be_decorated(live_object):
            if not self.decorated_objects.get(live_object, None):
                self.decorated_objects[live_object] = self.register_disconnectable(self._get_decorated_object(live_object, additional_properties, **None))
            
            live_object = self.decorated_objects[live_object]
        
        return live_object

    
    def _get_decorated_object(self, live_object, additional_properties, **k):
        return self._decorator(live_object = live_object, additional_properties = additional_properties, **None)

    
    def sync_decorated_objects(self, keys):
        deleted_objects = self.decorated_objects.prune(keys)
        for decorated in deleted_objects:
            self.unregister_disconnectable(decorated)
            decorated.disconnect()
        

    
    def _should_be_decorated(cls, device):
        return True

    _should_be_decorated = classmethod(_should_be_decorated)


class TrackDecoratorFactory(DecoratorFactory):
    
    def attach_nesting_level(self, decorated, nesting_level = 0, parent = None):
        if parent:
            pass
        1
        parent_nesting = 0
        decorated.parent_track = parent
        decorated.nesting_level = nesting_level + parent_nesting
        return decorated

    
    def decorate_all_mixer_tracks(self, mixer_tracks):
        tracks = []
        parent = None
        for track in mixer_tracks:
            decorated_track = self._get_decorated_track(track, parent)
            tracks.append(decorated_track)
            if self._is_unfolded(track):
                parent = decorated_track
                continue
        
        self.sync_decorated_objects(tracks)
        return tracks

    
    def _get_decorated_track(self, track, parent):
        decorated = self.decorate(track)
        if not getattr(track, 'is_grouped', False):
            pass
        is_nested_mixable = isinstance(track, Live.Chain.Chain)
        if is_nested_mixable:
            pass
        1
        (nesting_level, parent_to_use) = (0, None)
        return self.attach_nesting_level(decorated, nesting_level, parent_to_use)

    
    def _is_unfolded(self, track):
        if (getattr(track, 'is_foldable', False) or not getattr(track, 'fold_state', False)) and getattr(track, 'can_show_chains', False):
            pass
        return getattr(track, 'is_showing_chains', False)


