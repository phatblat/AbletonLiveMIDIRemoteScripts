# Source Generated with Decompyle++
# File: user_component.pyc (Python 2.5)

from ableton.v2.control_surface.control import ToggleButtonControl
from pushbase.user_component import UserComponentBase

class UserComponent(UserComponentBase):
    user_mode_toggle_button = ToggleButtonControl()
    
    def user_mode_toggle_button(self, toggled, button):
        self.toggle_mode()

    user_mode_toggle_button = user_mode_toggle_button.toggled(user_mode_toggle_button)

