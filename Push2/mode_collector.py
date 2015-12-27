# Source Generated with Decompyle++
# File: mode_collector.pyc (Python 2.5)

from ableton.v2.base import listenable_property, listens, Subject, SlotManager

class ModeCollector(SlotManager, Subject):
    
    def __init__(self, main_modes = None, mix_modes = None, global_mix_modes = None, device_modes = None, *a, **k):
        super(ModeCollector, self).__init__(*a, **a)
        self._main_modes = main_modes
        self._mix_modes = mix_modes
        self._global_mix_modes = global_mix_modes
        self._device_modes = device_modes
        self._on_selected_main_mode_changed.subject = main_modes
        self._on_selected_mix_mode_changed.subject = mix_modes
        self._on_selected_global_mix_mode_changed.subject = global_mix_modes
        self._on_selected_device_mode_changed.subject = device_modes

    
    def main_mode(self):
        return self._main_modes.selected_mode

    main_mode = listenable_property(main_mode)
    
    def _on_selected_main_mode_changed(self, mode):
        self.notify_main_mode()

    _on_selected_main_mode_changed = listens('selected_mode')(_on_selected_main_mode_changed)
    
    def mix_mode(self):
        return self._mix_modes.selected_mode

    mix_mode = listenable_property(mix_mode)
    
    def _on_selected_mix_mode_changed(self, mode):
        self.notify_mix_mode()

    _on_selected_mix_mode_changed = listens('selected_mode')(_on_selected_mix_mode_changed)
    
    def global_mix_mode(self):
        return self._global_mix_modes.selected_mode

    global_mix_mode = listenable_property(global_mix_mode)
    
    def _on_selected_global_mix_mode_changed(self, mode):
        self.notify_global_mix_mode()

    _on_selected_global_mix_mode_changed = listens('selected_mode')(_on_selected_global_mix_mode_changed)
    
    def device_mode(self):
        return self._device_modes.selected_mode

    device_mode = listenable_property(device_mode)
    
    def _on_selected_device_mode_changed(self, mode):
        self.notify_device_mode()

    _on_selected_device_mode_changed = listens('selected_mode')(_on_selected_device_mode_changed)

