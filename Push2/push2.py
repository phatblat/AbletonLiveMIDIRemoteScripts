# Source Generated with Decompyle++
# File: push2.pyc (Python 2.5)

from __future__ import with_statement
from contextlib import contextmanager
from functools import partial
import logging
import os
import sys
import Live
import MidiRemoteScript
from ableton.v2.base import const, inject, listens, listens_group, liveobj_valid, Subject, NamedTuple, Disconnectable
from ableton.v2.control_surface import BackgroundLayer, Component, IdentifiableControlSurface, Layer, get_element
from ableton.v2.control_surface.control import ButtonControl, DoubleClickContext
from ableton.v2.control_surface.elements import ButtonMatrixElement, ComboElement, SysexElement
from ableton.v2.control_surface.mode import EnablingModesComponent, ModeButtonBehaviour, ModesComponent, LayerMode, LazyComponentMode, ReenterBehaviour, SetAttributeMode
from pushbase.actions import select_clip_and_get_name_from_slot, select_scene_and_get_name
from pushbase.browser_modes import BrowserHotswapMode
from pushbase.quantization_component import QuantizationComponent, QuantizationSettingsComponent
from pushbase.selection import PushSelection
from pushbase.percussion_instrument_finder_component import find_drum_group_device
from pushbase import consts
from pushbase.push_base import PushBase, NUM_TRACKS, NUM_SCENES
from pushbase.track_frozen_mode import TrackFrozenModesComponent
from (null) import sysex
from actions import CaptureAndInsertSceneComponent
from automation import AutomationComponent
from elements import Elements
from browser_component import BrowserComponent, NewTrackBrowserComponent
from device_decoration import DeviceDecoratorFactory
from skin_default import make_default_skin
from mixer_component import MixerComponent
from device_component import DeviceComponent
from device_parameter_component import DeviceParameterComponent
from device_view_component import DeviceViewComponent
from device_navigation import is_empty_rack, DeviceNavigationComponent, MoveDeviceComponent
from drum_group_component import DrumGroupComponent
from drum_pad_parameter_component import DrumPadParameterComponent
from chain_selection_component import ChainSelectionComponent
from clip_control import AudioClipSettingsControllerComponent, ClipControlComponent, LoopSettingsControllerComponent
from clip_decoration import ClipDecoratorFactory
from colors import COLOR_TABLE
from convert import ConvertComponent, ConvertEnabler
from bank_selection_component import BankSelectionComponent
from firmware import FirmwareUpdateComponent, FirmwareVersion
from hardware_settings_component import HardwareSettingsComponent
from master_track import MasterTrackComponent
from mixer_control_component import MixerControlComponent
from note_settings import NoteSettingsComponent
from notification_component import NotificationComponent
from pad_velocity_curve import PadVelocityCurveSender
from scales_component import ScalesComponent, ScalesEnabler
from session_component import SessionComponent
from session_recording import SessionRecordingComponent
from session_ring_selection_linking import SessionRingSelectionLinking
from settings import create_settings
from stop_clip_component import StopClipComponent
from track_mixer_control_component import TrackMixerControlComponent
from mode_collector import ModeCollector
from setup_component import SetupComponent, Settings
from device_enabling import DeviceEnablingComponent
from track_selection import MixerTrackListComponent, SessionRingTrackProvider, ViewControlComponent
from user_component import UserComponent
from banking_util import BankingInfo
from custom_bank_definitions import BANK_DEFINITIONS
j = os.path.join
dn = os.path.dirname
sys.path.append(j(dn(dn(__file__)), '_Tools'))
import simplejson as json
logger = logging.getLogger(__name__)

class QmlError(Exception):
    pass


def make_dialog_layer(priority = consts.DIALOG_PRIORITY, *a, **k):
    return (BackgroundLayer('global_param_controls', 'select_buttons', 'track_state_buttons', priority = priority), Layer(priority = priority, *a, **a))


def tracks_to_use_from_song(song):
    return tuple(song.visible_tracks) + tuple(song.return_tracks)


def wrap_button(select_buttons, modifier):
    continue
    return [ ComboElement(button, modifier = modifier) for button in get_element(select_buttons) ]


def make_freeze_aware(component, layer, default_mode_extras = [], frozen_mode_extras = []):
    return TrackFrozenModesComponent(default_mode = [
        component,
        LayerMode(component, layer)] + default_mode_extras, frozen_mode = [
        component,
        LayerMode(component, Layer())] + frozen_mode_extras, is_enabled = False)


class RealTimeClientModel(Subject):
    __events__ = ('clientId',)
    
    def __init__(self):
        self._client_id = ''

    
    def _get_client_id(self):
        return self._client_id

    
    def _set_client_id(self, client_id):
        self._client_id = client_id
        self.notify_clientId()

    clientId = property(_get_client_id, _set_client_id)


class Push2(IdentifiableControlSurface, PushBase):
    session_component_type = SessionComponent
    drum_group_note_editor_skin = 'DrumGroupNoteEditor'
    input_target_name_for_auto_arm = 'Push2 Input'
    RESEND_MODEL_DATA_TIMEOUT = 5
    
    def __init__(self, c_instance = None, model = None, *a, **k):
        if not model is not None:
            raise AssertionError
        self._model = model
        self._double_click_context = DoubleClickContext()
        self._real_time_mapper = c_instance.real_time_mapper
        self._device_decorator_factory = DeviceDecoratorFactory()
        self._clip_decorator_factory = ClipDecoratorFactory()
        self._real_time_data_list = []
        super(Push2, self).__init__(c_instance = c_instance, product_id_bytes = sysex.IDENTITY_RESPONSE_PRODUCT_ID_BYTES, *a, **a)
        self._board_revision = 0
        self._firmware_version = FirmwareVersion(0, 0, 0)
        self._real_time_client = RealTimeClientModel()
        self._connected = False
        self._identified = False
        self._initialized = False
        self.register_disconnectable(model)
        self.register_disconnectable(self._device_decorator_factory)
        self.component_guard().__enter__()
        
        try:
            self._model.realTimeClient = self._real_time_client
            self._real_time_client.clientId = self._real_time_mapper.client_id
        finally:
            pass

        logger.info('Push 2 script loaded')

    
    def initialize(self):
        if not self._initialized:
            self._initialized = True
            self._init_hardware_settings()
            self._init_pad_curve()
            self._hardware_settings.fade_in_led_brightness(self._setup_settings.hardware.led_brightness)
            self._pad_curve_sender.send()
            self._send_color_palette()
            super(Push2, self).initialize()
            self._Push2__on_selected_track_frozen_changed.subject = self.song.view
            self._Push2__on_selected_track_frozen_changed()
            self._switch_to_live_mode()
            self._user.defer_sysex_sending = True
            self.update()
        
        if self._firmware_update.provided_version > self._firmware_version and self._board_revision > 0 and self._identified:
            self._firmware_update.start()
        

    
    def _try_initialize(self):
        if self._connected and self._identified:
            self.initialize()
        

    
    def on_process_state_changed(self, state):
        StateEnum = MidiRemoteScript.Push2ProcessState
        self._connected = state == StateEnum.connected
        if state == StateEnum.died:
            self._c_instance.launch_external_process()
        
        if state == StateEnum.connected:
            self.component_guard().__enter__()
            
            try:
                self._try_initialize()
            finally:
                pass

            self._model.commit_changes(send_all = True)
        

    
    def on_user_data_arrived(self, message):
        if self._initialized:
            data = json.loads(message)
            self._process_qml_errors(data)
            self._firmware_update.process_firmware_response(