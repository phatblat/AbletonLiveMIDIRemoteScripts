# Source Generated with Decompyle++
# File: pad_velocity_curve.pyc (Python 2.5)

import math
from ableton.v2.base import SerializableListenableProperties, chunks, clamp, listenable_property, task
from ableton.v2.control_surface import Component
NUM_VELOCITY_CURVE_ENTRIES = 128
LAST_INDEX_FOR_DISPLAY = 58

class LookupTable:
    MAXW = [
        1700,
        1660,
        1590,
        1510,
        1420,
        1300,
        1170,
        1030,
        860,
        640,
        400]
    CPMIN = [
        1650,
        1580,
        1500,
        1410,
        1320,
        1220,
        1110,
        1000,
        900,
        800,
        700]
    CPMAX = [
        2050,
        1950,
        1850,
        1750,
        1650,
        1570,
        1490,
        1400,
        1320,
        1240,
        1180]
    GAMMA = [
        0.7,
        0.64,
        0.58,
        0.54,
        0.5,
        0.46,
        0.43,
        0.4,
        0.36,
        0.32,
        0.25]
    MINV = [
        1,
        1,
        1,
        1,
        1,
        1,
        3,
        6,
        12,
        24,
        36]
    MAXV = [
        96,
        102,
        116,
        121,
        124,
        127,
        127,
        127,
        127,
        127,
        127]
    ALPHA = [
        90,
        70,
        54,
        40,
        28,
        20,
        10,
        -5,
        -25,
        -55,
        -90]


def gamma_func(x, gamma):
    return math.pow(x, math.exp(-4 + 8 * gamma))


def calculate_points(alpha):
    a1 = (225 - alpha) * math.pi / 180
    a2 = (45 - alpha) * math.pi / 180
    r = 0.4
    p1x = 0.5 + r * math.cos(a1)
    p1y = 0.5 + r * math.sin(a1)
    p2x = 0.5 + r * math.cos(a2)
    p2y = 0.5 + r * math.sin(a2)
    return (p1x, p1y, p2x, p2y)


def bezier(x, t, p1x, p1y, p2x, p2y):
    p0x = 0
    p0y = 0
    p3x = 1
    p3y = 1
    while t <= 1:
        s = 1 - t
        t2 = t * t
        t3 = t2 * t
        s2 = s * s
        s3 = s2 * s
        xt = s3 * p0x + 3 * t * s2 * p1x + 3 * t2 * s * p2x + t3 * p3x
        if xt >= x:
            return (s3 * p0y + 3 * t * s2 * p1y + 3 * t2 * s * p2y + t3 * p3y, t)
        
        t += 0.0001
    return (1, t)


def generate_velocity_curve(sensitivity, gain, dynamics):
    minw = 160
    maxw = LookupTable.MAXW[sensitivity]
    gamma = LookupTable.GAMMA[gain]
    minv = LookupTable.MINV[gain]
    maxv = LookupTable.MAXV[gain]
    alpha = LookupTable.ALPHA[dynamics]
    (p1x, p1y, p2x, p2y) = calculate_points(alpha)
    curve = []
    minw_index = int(minw) / 32
    maxw_index = int(maxw) / 32
    t = 0
    for index in xrange(NUM_VELOCITY_CURVE_ENTRIES):
        w = index * 32
        if w <= minw:
            velocity = 1 + (minv - 1) * float(index) / float(minw_index)
        elif w >= maxw:
            velocity = maxv + (127 - maxv) * float(index - maxw_index) / float(128 - maxw_index)
        else:
            wnorm = (w - minw) / (maxw - minw)
            (b, t) = bezier(wnorm, t, p1x, p1y, p2x, p2y)
            velonorm = gamma_func(b, gamma)
            velocity = minv + velonorm * (maxv - minv)
        curve.append(clamp(int(round(velocity)), 1, 127))
    
    return curve


def generate_thresholds(sensitivity, gain, dynamics):
    cpmin = LookupTable.CPMIN[sensitivity]
    cpmax = LookupTable.CPMAX[sensitivity]
    threshold0 = 33
    threshold1 = 31
    return (threshold0, threshold1, int(cpmin), int(cpmax))


class PadVelocityCurveSettings(SerializableListenableProperties):
    sensitivity = listenable_property.managed(5)
    min_sensitivity = 0
    max_sensitivity = 10
    gain = listenable_property.managed(5)
    min_gain = 0
    max_gain = 10
    dynamics = listenable_property.managed(5)
    min_dynamics = 0
    max_dynamics = 10


class PadVelocityCurveSender(Component):
    SEND_RATE = 0.5
    curve_points = listenable_property.managed([])
    
    def __init__(self, curve_sysex_element = None, threshold_sysex_element = None, settings = None, chunk_size = None, *a, **k):
        if not curve_sysex_element is not None:
            raise AssertionError
        if not threshold_sysex_element is not None:
            raise AssertionError
        if not settings is not None:
            raise AssertionError
        if not chunk_size is not None:
            raise AssertionError
        super(PadVelocityCurveSender, self).__init__(*a, **a)
        self._curve_sysex_element = curve_sysex_element
        self._threshold_sysex_element = threshold_sysex_element
        self._settings = settings
        self._chunk_size = chunk_size
        self._send_task = self._tasks.add(task.sequence(task.wait(self.SEND_RATE), task.run(self._on_send_task_finished))).kill()
        self._settings_changed = False
        self.register_slot(settings, self._on_setting_changed, 'sensitivity')
        self.register_slot(settings, self._on_setting_changed, 'gain')
        self.register_slot(settings, self._on_setting_changed, 'dynamics')
        self._update_curve_model()

    
    def send(self):
        self._send_velocity_curve()
        self._send_thresholds()
        self._settings_changed = False

    
    def _send_velocity_curve(self):
        velocities = self._generate_curve()
        velocity_chunks = chunks(velocities, self._chunk_size)
        for (index, velocities) in enumerate(velocity_chunks):
            self._curve_sysex_element.send_value(index * self._chunk_size, velocities)
        

    
    def _send_thresholds(self):
        threshold_values = generate_thresholds(self._settings.sensitivity, self._settings.gain, self._settings.dynamics)
        self._threshold_sysex_element.send_value(*threshold_values)

    
    def _generate_curve(self):
        return generate_velocity_curve(self._settings.sensitivity, self._settings.gain, self._settings.dynamics)

    
    def _on_setting_changed(self, _):
        if not self._send_task.is_running:
            self.send()
            self._send_task.restart()
        else:
            self._settings_changed = True
        self._update_curve_model()

    
    def _update_curve_model(self):
        self.curve_points = self._generate_curve()[:LAST_INDEX_FOR_DISPLAY]

    
    def _on_send_task_finished(self):
        if self._settings_changed:
            self.send()
        


