# coding: utf-8
""" Tabs, groups, conditions and hotkey placement: how to keep a panel with many
options readable.
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
        # a group: the master switch grays its children out when it is off
        templates.createControlsGroup(master, [
            templates.createSlider('Opacity', 'opacity', s.get('opacity', 80), 0, 100, 5,
                                   format='%d%%'),
            templates.createColorChoice('Color', 'color', s.get('color', 'E0A248')),
        ]),
        # shown only while the slider above is over 50, and it disappears rather than
        # graying out, so the panel closes the gap
        templates.visibleWhen(
            templates.createCheckbox('Warn when bright', 'warn', s.get('warn', False)),
            'opacity', 50, condition=CONDITION.GREATER, indent=True),
    ])


def soundTab():
    s = settings
    return templates.createTab('Sound', [
        templates.createCheckbox('Play a sound', 'sound', s.get('sound', False)),
        # grayed out, not hidden: the player can see the option exists
        templates.enableWhen(
            templates.createSlider('Volume', 'volume', s.get('volume', 50), 0, 100, 5),
            'sound', True, indent=True),
    ])


def keysTab():
    s = settings
    # A long label and its keys sit at opposite ends of the column by default, which
    # leaves a gap across the middle of a wide column. float= gives the keys a line of
    # their own instead.
    #
    # The two editions differ on 'right'. In the Flash edition the keys float and the
    # label flows around them; the Gameface engine has neither float nor shape-outside,
    # so there it means a line of its own against the right edge. 'below' is the same
    # line against the left edge, and reads the same in both.
    long = 'Switch to the next view while the battle loading screen is up'
    return templates.createTab('Keys', [
        templates.createHotkey('Short label', 'keyShort', s.get('keyShort', [])),
        templates.createHotkey(long, 'keyBelow', s.get('keyBelow', []), float='below'),
        templates.createHotkey(long, 'keyRight', s.get('keyRight', []), float='right'),
    ])


def template():
    return {
        'modDisplayName': 'Layout',
        'settingsVersion': 1,
        'enabled': settings.get('enabled', True),
        'tabs': [displayTab(), soundTab(), keysTab()],
    }


def init():
    global settings
    settings = g_modsSettingsApi.setModTemplate(LINKAGE, template(), onSettingsChanged)
