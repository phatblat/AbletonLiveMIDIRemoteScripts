# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.5)

from __future__ import absolute_import

def get_capabilities():
    caps = capabilities
    import ableton.v2.control_surface
    return {
        caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id = 10626, product_ids = [
            6503], model_name = 'Ableton Push 2'),
        caps.PORTS_KEY: [
            caps.inport(props = [
                caps.HIDDEN,
                caps.NOTES_CC,
                caps.SCRIPT]),
            caps.inport(props = []),
            caps.outport(props = [
                caps.HIDDEN,
                caps.NOTES_CC,
                caps.SYNC,
                caps.SCRIPT]),
            caps.outport(props = [])],
        caps.TYPE_KEY: 'push2',
        caps.AUTO_LOAD_KEY: True }


def create_instance(c_instance):
    Push2 = Push2
    import push2
    Root = Root
    Sender = Sender
    import push2_model
    root = Root(sender = Sender(logger = c_instance, message_sink = c_instance.send_model_update, process_connected = c_instance.process_connected))
    return Push2(c_instance = c_instance, model = root)

