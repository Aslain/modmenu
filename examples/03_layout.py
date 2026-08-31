# coding: utf-8
""" Tabs, groups and conditions: how to keep a panel with many options readable.
"""
from gui.aslainMenu import g_modsSettingsApi, templates
from gui.aslainMenu._constants import CONDITION

LINKAGE = 'example.layout'

settings = {}


def onSettingsChanged(linkage, newSettings):
    global settings
    settings = newSettings


def displayTab():
    s = settings
    master = templates.createCheckbox('Draw the panel', 'draw', s.get('draw', True))
    return templates.createTab('Display', [
        # a group: the master switch greys its children out when it is off
        templates.createControlsGroup(master, [
            templates.createSlider('Opacity', 'opacity', s.get('opacity', 80), 0, 100, 5,
                                   format='%d%%'),
            templates.createColorChoice('Colour', 'colour', s.get('colour', 'E0A248')),
        ]),
        # shown only while the slider above is over 50, and it disappears rather than
        # greying out, so the panel closes the gap
        templates.visibleWhen(
            templates.createCheckbox('Warn when bright', 'warn', s.get('warn', False)),
            'opacity', 50, condition=CONDITION.GREATER, indent=True),
    ])


def soundTab():
    s = settings
    return templates.createTab('Sound', [
        templates.createCheckbox('Play a sound', 'sound', s.get('sound', False)),
        # greyed out, not hidden: the player can see the option exists
        templates.enableWhen(
            templates.createSlider('Volume', 'volume', s.get('volume', 50), 0, 100, 5),
            'sound', True, indent=True),
    ])


def template():
    return {
        'modDisplayName': 'Layout',
        'settingsVersion': 1,
        'enabled': settings.get('enabled', True),
        'tabs': [displayTab(), soundTab()],
    }


def init():
    global settings
    settings = g_modsSettingsApi.setModTemplate(LINKAGE, template(), onSettingsChanged)
