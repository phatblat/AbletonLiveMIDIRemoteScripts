# Source Generated with Decompyle++
# File: session_recording.pyc (Python 2.5)

from __future__ import absolute_import
from pushbase.session_recording_component import FixedLengthSessionRecordingComponent

class SessionRecordingComponent(FixedLengthSessionRecordingComponent):
    
    def __init__(self, *a, **k):
        super(SessionRecordingComponent, self).__init__(*a, **a)
        self.set_trigger_recording_on_release(not (self._record_button.is_pressed))

    
    def set_trigger_recording_on_release(self, trigger_recording):
        self._should_trigger_recording = trigger_recording

    
    def _on_record_button_pressed(self):
        pass

    
    def _on_record_button_released(self):
        if self._should_trigger_recording:
            self._trigger_recording()
        
        self._should_trigger_recording = True


