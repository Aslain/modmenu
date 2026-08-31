# coding: utf-8
""" The smallest mod that has settings: two options, saved and read back.

Drop this in res_mods/<version>/scripts/client/gui/mods/ as mod_hello_modmenu.py
"""
import logging

_logger = logging.getLogger(__name__)

LINKAGE = 'example.hello'

# What the mod runs with before the player has touched anything, and what it falls back
# to when the menu is not installed at all.
settings = {'enabled': True, 'scale': 1.0}

# This menu first, then whatever else provides the API. The two names are not the same
# thing: gui.aslainMenu is this menu, gui.modsSettingsApi is whichever package claimed
# that name, which may be izeberg's original or the Flash edition. Asking in this order
# means a player who has both gets the new window.
try:
    from gui.aslainMenu import g_modsSettingsApi, templates
except ImportError:
    try:
        from gui.modsSettingsApi import g_modsSettingsApi, templates
    except ImportError:
        g_modsSettingsApi = None
        templates = None


def onSettingsChanged(linkage, newSettings):
    """ Called when the player presses Apply. """
    global settings
    settings = newSettings
    _logger.info('[hello] settings are now %s', settings)


def template():
    return {
        'modDisplayName': 'Hello Mod Menu',
        # raise this when you rename a key or change what one means
        'settingsVersion': 1,
        'enabled': settings['enabled'],
        'column1': [
            templates.createCheckbox(
                'Enabled', 'enabled', settings['enabled'],
                tooltip='{HEADER}Enabled{/HEADER}{BODY}Turns the whole thing off.{/BODY}'),
            templates.createSlider(
                'Scale', 'scale', settings['scale'], 0.5, 3.0, 0.05, format='%.2f'),
        ],
        'column2': [],
    }


def init():
    global settings
    if g_modsSettingsApi is None:
        _logger.info('[hello] no settings menu installed, running on defaults')
        return
    # setModTemplate registers the window AND returns what was saved, so one call is
    # enough to start with the player's own values.
    settings = g_modsSettingsApi.setModTemplate(LINKAGE, template(), onSettingsChanged)
