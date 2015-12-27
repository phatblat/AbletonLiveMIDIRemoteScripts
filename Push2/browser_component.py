# Source Generated with Decompyle++
# File: browser_component.pyc (Python 2.5)

from __future__ import with_statement
from contextlib import contextmanager
from itertools import imap
from math import ceil
import Live
from ableton.v2.base import BooleanContext, depends, index_if, lazy_attribute, listenable_property, listens, liveobj_changed, liveobj_valid, nop, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import control_list, ButtonControl, StepEncoderControl, ToggleButtonControl
from pushbase.browser_util import filter_type_for_hotswap_target, get_selection_for_new_device
from pushbase.message_box_component import Messenger
from colors import translate_color_index
from browser_list import BrowserList
from browser_item import BrowserItem, ProxyBrowserItem

class WrappedLoadableBrowserItem(BrowserItem):
    
    def __init__(self, *a, **k):
        super(WrappedLoadableBrowserItem, self).__init__(*a, **a)
        self._browser = Live.Application.get_application().browser

    
    def is_selected(self):
        if self._contained_item is None:
            return self._is_selected
        else:
            relation = self._browser.relation_to_hotswap_target(self._contained_item)
            return relation == Live.Browser.Relation.equal

    is_selected = property(is_selected)


class FolderBrowserItem(BrowserItem):
    
    def __init__(self, wrapped_loadable = None, *a, **k):
        if not wrapped_loadable is not None:
            raise AssertionError
        super(FolderBrowserItem, self).__init__(*a, **a)
        self._wrapped_loadable = wrapped_loadable

    
    def is_selected(self):
        if self._contained_item is None:
            pass
        1
        return self._contained_item.is_selected

    is_selected = property(is_selected)
    
    def children(self):
        return [
            self._wrapped_loadable] + list(self.contained_item.children)

    children = lazy_attribute(children)


class PluginPresetBrowserItem(BrowserItem):
    
    def __init__(self, preset_name = None, preset_index = None, vst_device = None, *a, **k):
        if not preset_name is not None:
            raise AssertionError
        if not preset_index is not None:
            raise AssertionError
        if not vst_device is not None:
            raise AssertionError
        if preset_name:
            pass
        1
        'name'(preset_name = '<Empty Slot %i>' % (preset_index + 1), is_loadable = True, *a, **a)
        self.preset_index = preset_index
        self._vst_device = vst_device

    
    def is_selected(self):
        return self._vst_device.selected_preset_index == self.preset_index

    is_selected = property(is_selected)
    
    def uri(self):
        return 'pluginpreset%i' % self.preset_index

    uri = property(uri)


class PluginBrowserItem(BrowserItem):
    
    def __init__(self, vst_device = None, *a, **k):
        super(PluginBrowserItem, self).__init__(is_loadable = False, is_selected = True, *a, **a)
        if not vst_device is not None:
            raise AssertionError
        self._vst_device = vst_device

    
    def children(self):
        continue
        return [ PluginPresetBrowserItem(preset_name = preset, preset_index = i, vst_device = self._vst_device) for (i, preset) in enumerate(self._vst_device.presets) ]

    children = property(children)


class CannotFocusListError(Exception):
    pass


class BrowserComponent(Component, Messenger):
    __events__ = ('loaded', 'close')
    NUM_ITEMS_PER_COLUMN = 6
    NUM_VISIBLE_BROWSER_LISTS = 7
    NUM_COLUMNS_IN_EXPANDED_LIST = 3
    EXPAND_LIST_TIME = 1.5
    REVEAL_PREVIEW_LIST_TIME = 0.2
    navigation_colors = dict(color = 'Browser.Navigation', disabled_color = 'Browser.NavigationDisabled')
    up_button = ButtonControl(repeat = True)
    down_button = ButtonControl(repeat = True)
    right_button = ButtonControl(repeat = True, **None)
    left_button = ButtonControl(repeat = True, **None)
    back_button = ButtonControl(**None)
    open_button = ButtonControl(**None)
    load_button = ButtonControl(**None)
    close_button = ButtonControl()
    prehear_button = ToggleButtonControl(toggled_color = 'Browser.Option', untoggled_color = 'Browser.OptionDisabled')
    scroll_encoders = control_list(StepEncoderControl, num_steps = 10, control_count = NUM_VISIBLE_BROWSER_LISTS)
    scroll_focused_encoder = StepEncoderControl(num_steps = 10)
    scrolling = listenable_property.managed(False)
    horizontal_navigation = listenable_property.managed(False)
    list_offset = listenable_property.managed(0)
    can_enter = listenable_property.managed(False)
    can_exit = listenable_property.managed(False)
    context_color_index = listenable_property.managed(-1)
    context_text = listenable_property.managed('')
    load_text = listenable_property.managed('')
    
    def __init__(self, preferences = dict(), commit_model_changes = None, selection = None, *a, **k):
        if not commit_model_changes is not None:
            raise AssertionError
        super(BrowserComponent, self).__init__(*a, **a)
        self._lists = []
        self._browser = Live.Application.get_application().browser
        self._current_hotswap_target = self._browser.hotswap_target
        self._updating_root_items = BooleanContext()
        self._focused_list_index = 0
        self._commit_model_changes = commit_model_changes
        self._preferences = preferences
        self._expanded = False
        self._unexpand_with_scroll_encoder = False
        self._delay_preview_list = BooleanContext()
        self._selection = selection
        self._load_next = False
        self._content_filter_type = None
        self._content_hotswap_target = None
        self._preview_list_task = self._tasks.add(task.sequence(task.wait(self.REVEAL_PREVIEW_LIST_TIME), task.run(self._replace_preview_list_by_task))).kill()
        self._update_root_items()
        self._update_navigation_buttons()
        self._update_load_text()
        self._update_context()
        self.prehear_button.is_toggled = preferences.setdefault('browser_prehear', True)
        self._on_selected_track_color_index_changed.subject = self.song.view
        self._on_selected_track_name_changed.subject = self.song.view
        self._on_hotswap_target_changed.subject = self._browser
        self.register_slot(self, self.notify_focused_item, 'focused_list_index')
        
        def auto_unexpand():
            self.expanded = False
            self._update_list_offset()

        self._unexpand_task = self._tasks.add(task.sequence(task.wait(self.EXPAND_LIST_TIME), task.run(auto_unexpand))).kill()

    __init__ = depends(commit_model_changes = None, selection = None)(__init__)
    
    def up_button(self, button):
        self._delay_preview_list().__enter__()
        
        try:
            self.focused_list.select_index_with_offset(-1)
        finally:
            pass

        self._update_auto_expand()
        self._update_scrolling()
        self._update_horizontal_navigation()

    up_button = up_button.pressed(up_button)
    
    def up_button(self, button):
        self._finish_preview_list_task()
        self._update_scrolling()

    up_button = up_button.released(up_button)
    
    def down_button(self, button):
        self._delay_preview_list().__enter__()
        
        try:
            self.focused_list.select_index_with_offset(1)
        finally:
            pass

        self._update_auto_expand()
        self._update_scrolling()
        self._update_horizontal_navigation()

    down_button = down_button.pressed(down_button)
    
    def down_button(self, button):
        self._finish_preview_list_task()
        self._update_scrolling()

    down_button = down_button.released(down_button)
    
    def right_button(self, button):
        if self._expanded and self._can_auto_expand() and self._focused_list_index > 0:
            self.focused_list.select_index_with_offset(self.NUM_ITEMS_PER_COLUMN)
            self._update_scrolling()
            self.horizontal_navigation = True
        elif not self._enter_selected_item():
            self._update_auto_expand()
        

    right_button = right_button.pressed(right_button)
    
    def right_button(self, button):
        self._update_scrolling()

    right_button = right_button.released(right_button)
    
    def left_button(self, button):
        if self._expanded and self._focused_list_index > 0 and self.focused_list.selected_index >= self.NUM_ITEMS_PER_COLUMN:
            self.focused_list.select_index_with_offset(-(self.NUM_ITEMS_PER_COLUMN))
            self._update_scrolling()
            self.horizontal_navigation = True
        else:
            self._exit_selected_item()

    left_button = left_button.pressed(left_button)
    
    def left_button(self, button):
        self._update_scrolling()

    left_button = left_button.released(left_button)
    
    def open_button(self, button):
        self._enter_selected_item()

    open_button = open_button.pressed(open_button)
    
    def back_button(self, button):
        self._exit_selected_item()

    back_button = back_button.pressed(back_button)
    
    def scroll_encoders(self, encoder):
        list_index = self._get_list_index_for_encoder(encoder)
        if list_index is not None:
            
            try:
                if self._focus_list_with_index(list_index, crop = False):
                    self._unexpand_with_scroll_encoder = True
                
                if self.focused_list.selected_item.is_loadable and encoder.index == self.scroll_encoders.control_count - 1:
                    self._update_list_offset()
                
                self._on_encoder_touched()
            except CannotFocusListError:
                pass
            


    scroll_encoders = scroll_encoders.touched(scroll_encoders)
    
    def scroll_encoders(self, encoders):
        self._on_encoder_released()

    scroll_encoders = scroll_encoders.released(scroll_encoders)
    
    def scroll_encoders(self, value, encoder):
        list_index = self._get_list_index_for_encoder(encoder)
        if list_index is not None:
            
            try:
                if self._focus_list_with_index(list_index):
                    self._unexpand_with_scroll_encoder = True
                
                self._on_encoder_value(value)
            except CannotFocusListError:
                pass
            


    scroll_encoders = scroll_encoders.value(scroll_encoders)
    
    def scroll_focused_encoder(self, value, encoder):
        self._on_encoder_value(value)

    scroll_focused_encoder = scroll_focused_encoder.value(scroll_focused_encoder)
    
    def scroll_focused_encoder(self, encoder):
        self._on_encoder_touched()

    scroll_focused_encoder = scroll_focused_encoder.touched(scroll_focused_encoder)
    
    def scroll_focused_encoder(self, encoder):
        self._on_encoder_released()

    scroll_focused_encoder = scroll_focused_encoder.released(scroll_focused_encoder)
    
    def _on_encoder_value(self, value):
        self._delay_preview_list().__enter__()
        
        try:
            self.focused_list.select_index_with_offset(value)
        finally:
            pass

        first_visible_list_focused = self.focused_list_index == self.list_offset
        if self.expanded and first_visible_list_focused:
            self.expanded = False
            self._unexpand_with_scroll_encoder = True
        elif not first_visible_list_focused and not (self.expanded) and self._can_auto_expand():
            self._update_auto_expand()
            self._unexpand_with_scroll_encoder = True
        
        self._update_scrolling()
        self._update_horizontal_navigation()

    
    def _on_encoder_touched(self):
        self._unexpand_task.kill()
        self._update_scrolling()
        self._update_horizontal_navigation()

    
    def _on_encoder_released(self):
        if not any(imap(lambda e: e.is_touched, self.scroll_encoders)):
            pass
        any_encoder_touched = self.scroll_focused_encoder.is_touched
        if not any_encoder_touched and self._unexpand_with_scroll_encoder:
            self._unexpand_task.restart()
        
        self._update_scrolling()

    
    def _get_list_index_for_encoder(self, encoder):
        if self.expanded:
            if encoder.index == 0:
                pass
            1
            return self.list_offset + 1
        else:
            index = self.list_offset + encoder.index
            if self.focused_list_index + 1 == index and self.focused_list.selected_item.is_loadable:
                index = self.focused_list_index
            
            if 0 <= index:
                pass
            index < len(self._lists)
            if 1:
                pass
            1
            return None

    
    def load_button(self, button):
        self._load_selected_item()

    load_button = load_button.pressed(load_button)
    
    def prehear_button(self, toggled, button):
        if toggled:
            self._prehear_selected_item()
        else:
            self._browser.stop_preview()
        self._preferences['browser_prehear'] = toggled
        self.notify_prehear_enabled()

    prehear_button = prehear_button.toggled(prehear_button)
    
    def close_button(self, button):
        self.notify_close()

    close_button = close_button.pressed(close_button)
    
    def lists(self):
        return self._lists

    lists = listenable_property(lists)
    
    def focused_list_index(self):
        return self._focused_list_index

    focused_list_index = listenable_property(focused_list_index)
    
    def prehear_enabled(self):
        return self.prehear_button.is_toggled

    prehear_enabled = listenable_property(prehear_enabled)
    
    def focused_list(self):
        return self._lists[self._focused_list_index]

    focused_list = property(focused_list)
    
    def focused_item(self):
        return self.focused_list.selected_item

    focused_item = listenable_property(focused_item)
    
    def expanded(self):
        return self._expanded

    expanded = listenable_property(expanded)
    
    def disconnect(self):
        super(BrowserComponent, self).disconnect()
        self._lists = []
        self._commit_model_changes = None

    
    def expanded(self, expanded):
        if self._expanded != expanded:
            self._expanded = expanded
            self._unexpand_with_scroll_encoder = False
            self._update_navigation_buttons()
            if len(self._lists) > self._focused_list_index + 1:
                self._lists[self._focused_list_index + 1].limit = self.num_preview_items
            
            self.notify_expanded()
        

    expanded = expanded.setter(expanded)
    
    def _on_selected_track_color_index_changed(self):
        if self.is_enabled():
            self._update_context()
            self._update_navigation_buttons()
        

    _on_selected_track_color_index_changed = listens('selected_track.color_index')(_on_selected_track_color_index_changed)
    
    def _on_selected_track_name_changed(self):
        if self.is_enabled():
            self._update_context()
        

    _on_selected_track_name_changed = listens('selected_track.name')(_on_selected_track_name_changed)
    
    def _on_hotswap_target_changed(self):
        if self.is_enabled():
            if not self._switched_to_empty_pad():
                self._update_root_items()
                self._update_context()
                self._update_list_offset()
            
        
        self._current_hotswap_target = self._browser.hotswap_target

    _on_hotswap_target_changed = listens('hotswap_target')(_on_hotswap_target_changed)
    
    def _switched_to_empty_pad(self):
        hotswap_target = self._browser.hotswap_target
        is_browsing_drumpad = isinstance(hotswap_target, Live.DrumPad.DrumPad)
        was_browsing_pad = isinstance(self._current_hotswap_target, Live.DrumPad.DrumPad)
        if is_browsing_drumpad and was_browsing_pad:
            pass
        return len(hotswap_target.chains) == 0

    
    def _focus_list_with_index(self, index, crop = True):
        '''
        Focus the list with the given index.
        Raises CannotFocusListError if the operation fails.
        Returns True if a new list was focused and False if it was already focused.
        '''
        if self._focused_list_index != index:
            if self._finish_preview_list_task():
                if index >= len(self._lists):
                    raise CannotFocusListError()
                
            
            if 0 <= index:
                pass
            index < len(self._lists)
            if not 1:
                raise AssertionError
            self._on_focused_selection_changed.subject = None
            if self._focused_list_index > index and crop:
                for l in self._lists[self._focused_list_index:]:
                    l.selected_index = -1
                
            
            self._focused_list_index = index
            self.focused_list.limit = -1
            if self.focused_list.selected_index == -1:
                self.focused_list.selected_index = 0
            
            self.notify_focused_list_index()
            self._on_focused_selection_changed.subject = self.focused_list
            if crop:
                self._crop_browser_lists(self._focused_list_index + 2)
            
            if self._focused_list_index == len(self._lists) - 1:
                self._replace_preview_list()
            
            self._reset_load_next()
            self._update_navigation_buttons()
            return True
        
        return False

    
    def _on_focused_selection_changed(self):
        if self._delay_preview_list and not (self.focused_item.is_loadable):
            self._preview_list_task.restart()
        else:
            self._replace_preview_list()
        self._update_navigation_buttons()
        self._prehear_selected_item()
        self._reset_load_next()
        self.notify_focused_item()

    _on_focused_selection_changed = listens('selected_index')(_on_focused_selection_changed)
    
    def _get_actual_item(self, item):
        contained_item = getattr(item, 'contained_item', None)
        if contained_item is not None:
            pass
        1
        return item

    
    def _load_selected_item(self):
        focused_list = self.focused_list
        if self._load_next:
            focused_list.selected_index += 1
        
        if focused_list.selected_index < len(focused_list.items) - 1:
            pass
        self._load_next = liveobj_valid(self._browser.hotswap_target)
        self._update_load_text()
        item = self._get_actual_item(focused_list.selected_item)
        notification_ref = self.show_notification(self._make_notification_text(item))
        self._commit_model_changes()
        self._load_item(item)
        self.notify_loaded()
        notification = notification_ref()
        if notification is not None:
            notification.reschedule_after_slow_operation()
        

    
    def _make_notification_text(self, browser_item):
        return 'Loading %s' % browser_item.name

    
    def _load_item(self, item):
        if liveobj_valid(self._browser.hotswap_target):
            if isinstance(item, PluginPresetBrowserItem):
                self._browser.hotswap_target.selected_preset_index = item.preset_index
            else:
                self._browser.load_item(item)
                self._content_hotswap_target = self._browser.hotswap_target
        else:
            self._insert_right_of_selected().__enter__()
            
            try:
                self._browser.load_item(item)
            finally:
                pass


    
    def _reset_load_next(self):
        self._load_next = False
        self._update_load_text()

    
    def _insert_right_of_selected(self):
        DeviceInsertMode = Live.Track.DeviceInsertMode
        device_to_select = get_selection_for_new_device(self._selection)
        if device_to_select:
            self._selection.selected_object = device_to_select
        
        selected_track_view = self.song.view.selected_track.view
        selected_track_view.device_insert_mode = DeviceInsertMode.selected_right
        yield None
        selected_track_view.device_insert_mode = DeviceInsertMode.default

    _insert_right_of_selected = contextmanager(_insert_right_of_selected)
    
    def _prehear_selected_item(self):
        if self.prehear_button.is_toggled and not (self._updating_root_items):
            self._browser.stop_preview()
            item = self._get_actual_item(self.focused_list.selected_item)
            if item and item.is_loadable and isinstance(item, Live.Browser.BrowserItem):
                self._browser.preview_item(item)
            
        

    
    def _stop_prehear(self):
        if self.prehear_button.is_toggled and not (self._updating_root_items):
            self._browser.stop_preview()
        

    
    def _update_load_text(self):
        if self._load_next:
            pass
        1
        self.load_text = 'Load'

    
    def _update_navigation_buttons(self):
        focused_list = self.focused_list
        self.up_button.enabled = focused_list.selected_index > 0
        self.down_button.enabled = focused_list.selected_index < len(focused_list.items) - 1
        selected_item_loadable = self.focused_list.selected_item.is_loadable
        if self._preview_list_task.is_running:
            pass
        assume_can_enter = not selected_item_loadable
        can_exit = self._focused_list_index > 0
        if not self._focused_list_index < len(self._lists) - 1:
            pass
        can_enter = assume_can_enter
        self.back_button.enabled = can_exit
        self.open_button.enabled = can_enter
        self.load_button.enabled = selected_item_loadable
        if self.context_color_index > -1:
            pass
        1
        context_button_color = 'Browser.Navigation'
        self.load_button.color = context_button_color
        self.close_button.color = context_button_color
        if not self._expanded:
            self.left_button.enabled = self.back_button.enabled
            if not can_enter:
                pass
            self.right_button.enabled = self._can_auto_expand()
        else:
            num_columns = int(ceil(float(len(self.focused_list.items)) / self.NUM_ITEMS_PER_COLUMN))
            last_column_start_index = (num_columns - 1) * self.NUM_ITEMS_PER_COLUMN
            self.left_button.enabled = self._focused_list_index > 0
            if not can_enter:
                pass
            self.right_button.enabled = self.focused_list.selected_index < last_column_start_index
        self.can_enter = can_enter
        self.can_exit = can_exit

    
    def _update_scrolling(self):
        if not self.up_button.is_pressed and self.down_button.is_pressed and self.scroll_focused_encoder.is_touched and any(imap(lambda e: e.is_touched, self.scroll_encoders)):
            if (self.right_button.is_pressed or self._expanded) and self.left_button.is_pressed:
                pass
        self.scrolling = self._expanded

    
    def _update_horizontal_navigation(self):
        if not self.right_button.is_pressed:
            pass
        self.horizontal_navigation = self.left_button.is_pressed

    
    def _update_context(self):
        selected_track = self.song.view.selected_track
        if liveobj_valid(self._browser.hotswap_target):
            self.context_text = self._browser.hotswap_target.name
        else:
            self.context_text = selected_track.name
        selected_track_color_index = selected_track.color_index
        if selected_track_color_index is not None:
            pass
        1
        self.context_color_index = -1

    
    def _enter_selected_item(self):
        item_entered = False
        self._finish_preview_list_task()
        new_index = self._focused_list_index + 1
        if 0 <= new_index:
            pass
        new_index < len(self._lists)
        if 1:
            self._focus_list_with_index(new_index)
            self._unexpand_task.kill()
            self._update_list_offset()
            self._update_auto_expand()
            self._prehear_selected_item()
            item_entered = True
        
        return item_entered

    
    def _exit_selected_item(self):
        item_exited = False
        
        try:
            self._focus_list_with_index(self._f