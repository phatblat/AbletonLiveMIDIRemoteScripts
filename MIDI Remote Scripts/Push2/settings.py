# Source Generated with Decompyle++
# File: settings.pyc (Python 2.5)

from pushbase.setting import OnOffSetting

def create_settings(preferences = None):
    if preferences is not None:
        pass
    1
    preferences = { }
    return {
        'workflow': OnOffSetting(name = 'Workflow', value_labels = [
            'Scene',
            'Clip'], default_value = True, preferences = preferences) }

