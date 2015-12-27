# Source Generated with Decompyle++
# File: device_navigation.pyc (Python 2.5)

from __future__ import absolute_import, with_statement
from contextlib import contextmanager
from itertools import ifilter, imap, chain
from functools import partial
from _Tools.multipledispatch import dispatch
import Live
from ableton.v2.base import find_if, first, index_if, listenable_property, listens, listens_group, liveobj_changed, liveobj_valid, SlotGroup, SlotManager, Subject, task
from ableton.v2.control_surface.control import control_list, forward_control, StepEncoderControl
from ableton.v2.control_surface.mode import Component, ModesComponent
from pushbase.device_chain_utils import is_first_device_on_pad
from decoration import DecoratorFactory
from item_lister_component import ItemListerComponent, ItemProvider

def find_drum_pad(items):
    elements = imap(lambda i: i.item, items)
    return find_if(lambda e: is_drum_pad(e), elements)


def is_empty_rack(rack):
    if rack.can_have_chains:
        pass
    return len(rack.chains) == 0


def is_active_element(drum_pad):
    if not (drum_pad.mute):
        pass
    return drum_pad.canonical_parent.is_active

is_active_element = dispatch(Live.DrumPad.DrumPad)(is_active_element)

def is_active_element(device):
    return device.is_active

is_active_element = dispatch(object)(is_active_element)

def nested_device_parent(device):
    if device.can_have_chains and device.view.is_showing_chain_devices and not (device.view.is_collapsed):
        pass
    1


def collect_devices(track_or_chain, nesting_level = 0):
    if liveobj_valid(track_or_chain):
        pass
    1
    chain_devices = []
    devices = []
    for device in chain_devices:
        devices.append((device, nesting_level))
        if device.can_have_drum_pads and device.view.selected_drum_pad:
            devices.append((device.view.selected_drum_pad, nesting_level + 1))
        
        devices.extend(collect_devices(nested_device_parent(device), nesting_level = nesting_level + 1))
    
    return devices


def delete_device(device):
    device_parent = device.canonical_parent
    device_index = list(device_parent.devices).index(device)
    device_parent.delete_device(device_index)


class FlattenedDeviceChain(SlotManager, ItemProvider):
    
    def __init__(self, *a, **k):
        super(FlattenedDeviceChain, self).__init__(*a, **a)
        self._device_parent = None
        self._devices = []
        self._selected_item = None
        
        def make_slot_group(event):
            slot_group = SlotGroup(self._update_devices, event)
            return self.register_slot_manager(slot_group)

        self._devices_changed = make_slot_group('devices')
        self._selected_chain_changed = make_slot_group('selected_chain')
        self._selected_pad_changed = make_slot_group('selected_drum_pad')
        self._collapsed_state_changed = make_slot_group('is_collapsed')
        self._chain_devices_visibility_changed = make_slot_group('is_showing_chain_devices')

    
    def items(self):
        return self._devices

    items = property(items)
    
    def _get_selected_item(self):
        return self._selected_item

    
    def _set_selected_item(self, device):
        if liveobj_changed(self._selected_item, device):
            self._selected_item = device
            self.notify_selected_item()
        

    selected_item = property(_get_selected_item, _set_selected_item)
    
    def has_invalid_selection(self):
        return not liveobj_valid(self._selected_item)

    has_invalid_selection = property(has_invalid_selection)
    
    def set_device_parent(self, parent):
        self._device_parent = parent
        self._update_devices()

    
    def _update_devices(self, *_):
        self._devices = collect_devices(self._device_parent)
        self._update_listeners()
        self.notify_items()

    
    def _update_listeners(self):
        
        def get_rack_views(racks):
            return map(lambda x: first(x).view, racks)

        racks = filter(lambda x: getattr(first(x), 'can_have_chains', False), self._devices)
        rack_views = get_rack_views(racks)
        device_parents = chain(imap(lambda x: x.selected_chain, rack_views), [
            self._device_parent])
        
        def is_empty_pad_drum_rack(item):
            rack = first(item)
            if rack.can_have_drum_pads and rack.view.selected_drum_pad:
                pass
            return len(rack.view.selected_drum_pad.chains) == 0

        empty_pad_drum_rack_views = get_rack_views(ifilter(is_empty_pad_drum_rack, racks))
        self._devices_changed.replace_subjects(device_parents)
        self._selected_chain_changed.replace_subjects(rack_views)
        self._collapsed_state_changed.replace_subjects(rack_views)
        self._chain_devices_visibility_changed.replace_subjects(rack_views)
        self._selected_pad_changed.replace_subjects(empty_pad_drum_rack_views)



def is_drum_pad(item):
    if liveobj_valid(item):
        pass
    return isinstance(item, Live.DrumPad.DrumPad)


def drum_rack_for_pad(drum_pad):
    return drum_pad.canonical_parent


class DeviceChainEnabledStateWatcher(Subject, SlotManager):
    __events__ = ('enabled_state',)
    
    def __init__(self, device_navigation = None, *a, **k):
        if not device_navigation is not None:
            raise AssertionError
        super(DeviceChainEnabledStateWatcher, self).__init__(*a, **a)
        self._device_navigation = device_navigation
        self._DeviceChainEnabledStateWatcher__on_items_changed.subject = device_navigation
        self._update_listeners_and_notify()

    
    def __on_items_changed(self, *a):
        self._update_listeners_and_notify()

    _DeviceChainEnabledStateWatcher__on_items_changed = listens('items')(__on_items_changed)
    
    def __on_is_active_changed(self, device):
        self._notify()

    _DeviceChainEnabledStateWatcher__on_is_active_changed = listens_group('is_active')(__on_is_active_changed)
    
    def __on_mute_changed(self):
        self._notify()

    _DeviceChainEnabledStateWatcher__on_mute_changed = listens('mute')(__on_mute_changed)
    
    def _navigation_items(self):
        return ifilter(lambda i: not (i.is_scrolling_indicator), self._device_navigation.items)

    
    def _devices(self):
        device_items = ifilter(lambda i: not is_drum_pad(i.item), self._navigation_items())
        return map(lambda i: i.item, device_items)

    
    def _update_listeners_and_notify(self):
        self._DeviceChainEnabledStateWatcher__on_is_active_changed.replace_subjects(self._devices())
        self._DeviceChainEnabledStateWatcher__on_mute_changed.subject = find_drum_pad(self._navigation_items())
        self._notify()

    
    def _notify(self):
        self.notify_enabled_state()



class MoveDeviceComponent(Component):
    MOVE_DELAY = 0.1
    move_encoders = control_list(StepEncoderControl)
    
    def __init__(self, *a, **k):
        super(MoveDeviceComponent, self).__init__(*a, **a)
        self._device = None

    
    def set_device(self, device):
        self._device = device

    
    def move_encoders(self, value, encoder):
        if self._device is not None:
            self._disabled_encoders().__enter__()
            
            try:
                if value > 0:
                    self._move_right()
                else:
                    self._move_left()
            finally:
                pass

        

    move_encoders = move_encoders.value(move_encoders)
    
    def _disabled_encoders(self):
        self._disable_all_encoders()
        yield None
        self._tasks.add(task.sequence(task.wait(self.MOVE_DELAY), task.run(self._enable_all_encoders)))

    _disabled_encoders = contextmanager(_disabled_encoders)
    
    def _disable_all_encoders(self):
        for encoder in self.move_encoders:
            encoder.enabled = False
        

    
    def _enable_all_encoders(self):
        for encoder in self.move_encoders:
            encoder.enabled = True
        

    
    def _move_right(self):
        parent = self._device.canonical_parent
        device_index = list(parent.devices).index(self._device)
        if device_index == len(parent.devices) - 1 and isinstance(parent, Live.Chain.Chain):
            self._move_out(parent.canonical_parent, move_behind = True)
        elif device_index < len(parent.devices) - 1:
            right_device = parent.devices[device_index + 1]
            if right_device.can_have_chains and right_device.view.is_showing_chain_devices and right_device.view.selected_chain:
                self._move_in(right_device)
            else:
                self.song.move_device(self._device, parent, device_index + 2)
        

    
    def _move_left(self):
        parent = self._device.canonical_parent
        device_index = list(parent.devices).index(self._device)
        if device_index > 0:
            left_device = parent.devices[device_index - 1]
            if left_device.can_have_chains and left_device.view.is_showing_chain_devices and left_device.view.selected_chain:
                self._move_in(left_device, move_to_end = True)
            else:
                self.song.move_device(self._device, parent, device_index - 1)
        elif isinstance(parent, Live.Chain.Chain):
            self._move_out(parent.canonical_parent)
        

    
    def _move_out(self, rack, move_behind = False):
        parent = rack.canonical_parent
        rack_index = list(parent.devices).index(rack)
        if move_behind:
            pass
        1
        self._device(parent, rack_index + 1, rack_index)

    
    def _move_in(self, rack, move_to_end = False):
        chain = rack.view.selected_chain
        if chain:
            if move_to_end:
                pass
            1
            self._device(chain, len(chain.devices), 0)
        



class DeviceNavigationComponent(ItemListerComponent):
    __events__ = ('drum_pad_selection',)
    select_buttons = forward_control(ItemListerComponent.select_buttons)
    
    def __init__(self, device_bank_registry = None, device_component = None, delete_handler = None, chain_selection = None, bank_selection = None, move_device = None, track_selection = None, *a, **k):
        if not device_bank_registry is not None:
            raise AssertionError
        if not device_component is not None:
            raise AssertionError
        if not chain_selection is not None:
            raise AssertionError
        if not bank_selection is not None:
            raise AssertionError
        if not move_device is not None:
            raise AssertionError
        self._flattened_chain = FlattenedDeviceChain()
        super(DeviceNavigationComponent, self).__init__(item_provider = self._flattened_chain, *a, **a)
        self._track_decorator = DecoratorFactory()
        self._device_component = device_component
        self._DeviceNavigationComponent__on_device_changed.subject = device_component
        self._DeviceNavigationComponent__on_device_changed()
        self._device_bank_registry = device_bank_registry
        self._delete_handler = delete_handler
        self._chain_selection = self.register_component(chain_selection)
        self._bank_selection = self.register_component(bank_selection)
        self._move_device = self.register_component(move_device)
        self._last_pressed_button_index = -1
        self._selected_on_previous_press = None
        self._modes = self.register_component(ModesComponent())
        self._modes.add_mode('default', [
            track_selection,
            partial(self._chain_selection.set_parent, None),
            partial(self._bank_selection.set_device, None)])
        self._modes.add_mode('chain_selection', [
            self._chain_selection])
        self._modes.add_mode('bank_selection', [
            self._bank_selection])
        self._modes.selected_mode = 'default'
        self.register_disconnectable(self._flattened_chain)
        self._DeviceNavigationComponent__on_items_changed.subject = self
        self._DeviceNavigationComponent__on_bank_selection_closed.subject = self._bank_selection
        self._on_selected_track_changed()
        self._on_selected_track_changed.subject = self.song.view
        watcher = self.register_disconnectable(DeviceChainEnabledStateWatcher(device_navigation = self))
        self._DeviceNavigationComponent__on_enabled_state_changed.subject = watcher
        self._update_button_colors()

    
    def modes(self):
        return self._modes

    modes = property(modes)
    
    def select_buttons(self, button):
        self._last_pressed_button_index = button.index
        device_or_pad = self.items[button.index].item
        if not (self._delete_handler) or not (self._delete_handler.is_deleting):
            if self.selected_object != device_or_pad:
                pass
            1
            self._selected_on_previous_press = None
            self._select_item(device_or_pad)
        

    select_buttons = select_buttons.pressed(select_buttons)
    
    def select_buttons(self, button):
        self._last_pressed_button_index = -1
        device_or_pad = self.items[button.index].item
        if self._delete_handler and self._delete_handler.is_deleting:
            self._delete_item(device_or_pad)
        elif self.selected_object == device_or_pad and device_or_pad != self._selected_on_previous_press:
            self._on_reselecting_object(device_or_pad)
        
        self._selected_on_previous_press = None

    select_buttons = select_buttons.released_immediately(select_buttons)
    
    def select_buttons(self, button):
        self._on_pressed_delayed(self.items[button.index].item)

    select_buttons = select_buttons.pressed_delayed(select_buttons)
    
    def select_buttons(self, button):
        if button.index == self._last_pressed_button_index:
            self._modes.selected_mode = 'default'
            self._last_pressed_button_index = -1
            self._end_move_device()
        

    select_buttons = select_buttons.released(select_buttons)
    
    def __on_enabled_state_changed(self):
        self._update_button_colors()

    _DeviceNavigationComponent__on_enabled_state_changed = listens('enabled_state')(__on_enabled_state_changed)
    
    def __on_items_changed(self):
        new_items = map(lambda x: x.item, self.items)
        if new_items and is_drum_pad(new_items[-1]):
            pass
        lost_selection_on_empty_pad = self._flattened_chain.selected_item not in new_items
        if self._should_select_drum_pad() or lost_selection_on_empty_pad:
            self._select_item(self._current_drum_pad())
        
        if self.moving:
            self._show_selected_item()
        
        self.notify_drum_pad_selection()

    _DeviceNavigationComponent__on_items_changed = listens('items')(__on_items_changed)
    
    def moving(self):
        return self._move_device.is_enabled()

    moving = listenable_property(moving)
    
    def device_selection_update_allowed(self):
        return not self._should_select_drum_pad()

    device_selection_update_allowed = property(device_selection_update_allowed)
    
    def _update_button_colors(self):
        for button in self.select_buttons:
            item = self.items[button.index]
            device_or_pad = item.item
            if liveobj_valid(device_or_pad):
                pass
            is_active = is_active_element(device_or_pad)
            if is_active:
                pass
            1
            button.unchecked_color = 'DefaultButton.Off'
        

    
    def _begin_move_device(self, device):
        if not self._move_device.is_enabled() and device.type != Live.Device.DeviceType.instrument:
            self._move_device.set_device(device)
            self._move_device.set_enabled(True)
            self._scroll_overlay.set_enabled(False)
            self.notify_moving()
        

    
    def _end_move_device(self):
        if self._move_device.is_enabled():
            self._move_device.set_device(None)
            self._move_device.set_enabled(False)
            self._scroll_overlay.set_enabled(True)
            self.notify_moving()
        

    
    def _show_selected_item(self):
        selected_item = self.item_provider.selected_item
        if selected_item is not None:
            items = self.item_provider.items
            if len(items) > self._num_visible_items:
                selected_index = (index_if,)(lambda i: i[0] == selected_item, items)
                if selected_index >= self._num_visible_items + self.item_offset - 1 and selected_index < len(items) - 1:
                    self.item_offset = (selected_index - self._num_visible_items) + 2
                elif selected_index > 0 and selected_index <= self.item_offset:
                    self.item_offset = selected_index - 1
                
            
        

    
    def request_drum_pad_selection(self):
        self._current_track().drum_pad_selected = True

    
    def unfold_current_drum_pad(self):
        self._current_track().drum_pad_selected = False
        self._current_drum_pad().canonical_parent.view.is_showing_chain_devices = True

    
    def is_drum_pad_selected(self):
        return is_drum_pad(self._flattened_chain.selected_item)

    is_drum_pad_selected = property(is_drum_pad_selected)
    
    def is_drum_pad_unfolded(self):
        selection = self._flattened_chain.selected_item
        if not is_drum_pad(selection):
            raise AssertionError
        return drum_rack_for_pad(selection).view.is_showing_chain_devices

    is_drum_pad_unfolded = property(is_drum_pad_unfolded)
    
    def _current_track(self):
        return self._track_decorator.decorate(self.song.view.selected_track, additional_properties = {
            'drum_pad_selected': False })

    
    def _should_select_drum_pad(self):
        return self._current_track().drum_pad_selected

    
    def _current_drum_pad(self):
        return find_drum_pad(self.items)

    
    def _on_selected_track_changed(self):
        self._selected_track = self.song.view.selected_track
        selected_track = self._current_track()
        self.reset_offset()
        self._flattened_chain.set_device_parent(selected_track)
        self._device_selection_in_track_changed.subject = selected_track.view
        self._modes.selected_mode = 'default'
        self._end_move_device()
        self._restore_selection(selected_track)

    _on_selected_track_changed = listens('selected_track')(_on_selected_track_changed)
    
    def _restore_selection(self, selected_track):
        to_select = None
        if self._should_select_drum_pad():
            to_select = self._current_drum_pad()
        
        if to_select == None:
            to_select = selected_track.view.selected_device
        
        self._select_item(to_select)

    
    def back_to_top(self):
        pass

    
    def selected_object(self):
        selected_item = self.item_provider.selected_item
        return getattr(selected_item, 'proxied_object', selected_item)

    selected_object = property(selected_object)
    
    def _select_item(self, device_or_pad):
        if device_or_pad:
            self._do_select_item(device_or_pad)
        
        self._update_item_provider(device_or_pad)

    
    def _do_select_item(self, pad):
        self._current_track().drum_pad_selected = True
        device = self._first_device_on_pad(pad)
        self._appoint_device(device)

    _do_select_item = dispatch(Live.DrumPad.DrumPad)(_do_select_item)
    
    def _first_device_on_pad(self, drum_pad):
        chain = drum_rack_for_pad(drum_pad).view.selected_chain
        if chain and chain.devices:
            return first(chain.devices)
        

    
    def _appoint_device(self, device):
        if self._device_component._device_changed(device):
            self._device_component.set_device(device)
        

    
    def _do_select_item(self, device):
        self._current_track().drum_pad_selected = False
        self.song.view.select_device(device)
        if device.can_be_appointed:
            self._appoint_device(device)
        

    _do_select_item = dispatch(object)(_do_select_item)
    
    def _on_reselecting_object(self, drum_pad):
        rack = drum_rack_for_pad(drum_pad)
        self._toggle(rack)
        if rack.view.is_showing_chain_devices:
            first_device = self._first_device_on_pad(drum_pad)
            if first_device:
                self._select_item(first_device)
            
        
        self.notify_drum_pad_selection()

    _on_reselecting_object = dispatch(Live.DrumPad.DrumPad)(_on_reselecting_object)
    
    def _on_reselecting_object(self, device):
        if liveobj_valid(device) and device.can_have_chains:
            if not device.can_have_drum_pads:
                self._toggle(device)
            
        else:
            self._bank_selection.set_device(device)
            self._modes.selected_mode = 'bank_selection'

    _on_reselecting_object = dispatch(object)(_on_reselecting_object)
    
    def _on_pressed_delayed(self, _):
        pass

    _on_pressed_delayed = dispatch(Live.DrumPad.DrumPad)(_on_pressed_delayed)
    
    def _on_pressed_delayed(self, device):
        self._show_chains(device)
        self._begin_move_device(device)

    _on_pressed_delayed = dispatch(object)(_on_pressed_delayed)
    
    def _delete_item(self, pad):
        pass

    _delete_item = dispatch(Live.DrumPad.DrumPad)(_delete_item)
    
    def _delete_item(self, device):
        delete_device(device)

    _delete_item = dispatch(object)(_delete_item)
    
    def _show_chains(self, device):
        if device.can_have_chains:
            self._chain_selection.set_parent(device)
            self._modes.selected_mode = 'chain_selection'
        

    
    def __on_bank_selection_closed(self):
        self._modes.selected_mode = 'default'

    _DeviceNavigationComponent__on_bank_selection_closed = listens('back')(__on_bank_selection_closed)
    
    def __on_device_changed(self):
        if not self._should_select_drum_pad() and self._flattened_chain.has_invalid_selection:
            self._update_item_provider(self._device_component.device())
        

    _DeviceNavigationComponent__on_device_changed = listens('device')(__on_device_changed)
    
    def _device_selection_in_track_changed(self):
        new_selection = self.song.view.selected_track.view.selected_device
        if self._can_update_device_selection(new_selection):
            self._modes.selected_mode = 'default'
            self._update_item_provider(new_selection)
        

    _device_selection_in_track_changed = listens('selected_device')(_device_selection_in_track_changed)
    
    def _toggle(self, item):
        view = item.view
        if view.is_collapsed:
            view.is_collapsed = False
            view.is_showing_chain_devices = True
        else:
            view.is_showing_chain_devices = not (view.is_showing_chain_devices)

    
    def _can_update_device_selection(self, new_selection):
        can_update = liveobj_valid(new_selection)
        if not self.is_drum_pad_selected:
            pass
        drum_pad_selected_or_requested = self._should_select_drum_pad()
        if can_update and drum_pad_selected_or_requested:
            if is_empty_rack(new_selection):
                can_update = False
            
            if can_update and self.is_drum_pad_selected:
                can_update = not is_first_device_on_pad(new_selection, self._flattened_chain.selected_item)
            
        elif not can_update and not drum_pad_selected_or_requested:
            can_update = True
        
        return can_update

    
    def _update_item_provider(self, selection):
        self._flattened_chain.selected_item = selection
        if not is_drum_pad(selection):
            self._current_track().drum_pad_selected = False
        
        self.notify_drum_pad_selection()


