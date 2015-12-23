# Source Generated with Decompyle++
# File: browser_item.pyc (Python 2.5)

from ableton.v2.base import Proxy

class BrowserItem(object):
    
    def __init__(self, name = '', icon = '', children = None, is_loadable = False, is_selected = False, contained_item = None, enable_wrapping = True, *a, **k):
        super(BrowserItem, self).__init__(*a, **a)
        self._name = name
        self._icon = icon
        if children is None:
            pass
        1
        self._children = children
        self._is_loadable = is_loadable
        self._is_selected = is_selected
        self._contained_item = contained_item
        self._enable_wrapping = enable_wrapping

    
    def name(self):
        return self._name

    name = property(name)
    
    def icon(self):
        return self._icon

    icon = property(icon)
    
    def children(self):
        return self._children

    children = property(children)
    
    def iter_children(self):
        return self.children

    iter_children = property(iter_children)
    
    def is_loadable(self):
        return self._is_loadable

    is_loadable = property(is_loadable)
    
    def is_selected(self):
        return self._is_selected

    is_selected = property(is_selected)
    
    def contained_item(self):
        return self._contained_item

    contained_item = property(contained_item)
    
    def is_device(self):
        return False

    is_device = property(is_device)
    
    def enable_wrapping(self):
        return self._enable_wrapping

    enable_wrapping = property(enable_wrapping)
    
    def uri(self):
        if self._contained_item is not None:
            pass
        1
        return self._name

    uri = property(uri)


class ProxyBrowserItem(Proxy):
    
    def __init__(self, enable_wrapping = True, icon = '', *a, **k):
        super(ProxyBrowserItem, self).__init__(*a, **a)
        self._enable_wrapping = enable_wrapping
        self._icon = icon

    
    def icon(self):
        return self._icon

    icon = property(icon)
    
    def enable_wrapping(self):
        return self._enable_wrapping

    enable_wrapping = property(enable_wrapping)
    
    def contained_item(self):
        return self.proxied_object

    contained_item = property(contained_item)

