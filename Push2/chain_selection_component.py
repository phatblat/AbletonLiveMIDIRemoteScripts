# Source Generated with Decompyle++
# File: chain_selection_component.pyc (Python 2.5)

from __future__ import absolute_import
from ableton.v2.base import SlotManager, listens, liveobj_valid
from ableton.v2.control_surface.control import forward_control
from item_lister_component import ItemListerComponent, ItemProvider

class ChainProvider(SlotManager, ItemProvider):
    
    def __init__(self, *a, **k):
        super(ChainProvider, self).__init__(*a, **a)
        self._rack = None

    
    def set_rack(self, rack):
        if rack != self._rack:
            if rack:
                pass
            1
            rack_view = None
            self._rack = rack
            self._ChainProvider__on_chains_changed.subject = rack
            self._ChainProvider__on_selected_chain_changed.subject = rack_view
            self.notify_items()
            self.notify_selected_item()
        

    
    def items(self):
        if liveobj_valid(self._rack):
            pass
        1
        chains = []
        continue
        return [ (chain, 0) for chain in chains ]

    items = property(items)
    
    def selected_item(self):
        if liveobj_valid(self._rack):
            pass
        1

    selected_item = property(selected_item)
    
    def select_chain(self, chain):
        self._rack.view.selected_chain = chain

    
    def __on_chains_changed(self):
        self.notify_items()

    _ChainProvider__on_chains_changed = listens('chains')(__on_chains_changed)
    
    def __on_selected_chain_changed(self):
        self.notify_selected_item()

    _ChainProvider__on_selected_chain_changed = listens('selected_chain')(__on_selected_chain_changed)


class ChainSelectionComponent(ItemListerComponent):
    select_buttons = forward_control(ItemListerComponent.select_buttons)
    
    def __init__(self, *a, **k):
        self._chain_parent = ChainProvider()
        super(ChainSelectionComponent, self).__init__(item_provider = self._chain_parent, *a, **a)
        self.register_disconnectable(self._chain_parent)

    
    def select_buttons(self, button):
        self._chain_parent.select_chain(self.items[button.index].item)

    select_buttons = select_buttons.checked(select_buttons)
    
    def set_parent(self, parent):
        if not parent is None and parent.can_have_chains:
            raise AssertionError
        self._chain_parent.set_rack(parent)


