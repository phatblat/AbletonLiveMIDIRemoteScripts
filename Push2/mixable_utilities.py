# Source Generated with Decompyle++
# File: mixable_utilities.pyc (Python 2.5)

import Live
from pushbase.device_chain_utils import find_instrument_meeting_requirement

def is_chain(track_or_chain):
    return isinstance(getattr(track_or_chain, 'proxied_object', track_or_chain), Live.Chain.Chain)


def is_midi_track(track):
    if getattr(track, 'has_midi_input', False):
        pass
    return not is_chain(track)


def is_audio_track(track):
    if getattr(track, 'has_audio_input', False):
        pass
    return not is_chain(track)


def can_play_clips(mixable):
    return hasattr(mixable, 'fired_slot_index')


def find_drum_rack_instrument(track):
    return find_instrument_meeting_requirement(lambda i: i.can_have_drum_pads, track)


def find_simpler(track_or_chain):
    return find_instrument_meeting_requirement(lambda i: hasattr(i, 'playback_mode'), track_or_chain)

