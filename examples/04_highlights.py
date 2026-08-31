# coding: utf-8
""" Marking options as new, and the three ways a highlight goes away or comes back.

A highlighted option gets a red flare on its row and adds one to a red counter beside
the mod's name in the list. The window clears a flare as soon as the user clicks the row
or changes the value, and remembers that per user, so the same option never nags twice.

A mod being installed for the first time never lights up. Everything in it is new to the
user anyway, and a fresh install that greets you with twenty flares is noise, not news.
Only options added to a mod that was already there light up. That makes highlights hard
to look at on purpose, which is why the buttons below exist: they put the window back
into the state a returning user would see.
"""
from gui.aslainMenu import g_modsSettingsApi, templates

LINKAGE = 'example.highlights'

# Stands in for a real mod's release number. Bumping the token re-lights the one control
# that carries it, even for users who already dismissed it, which is what you want when
# an option's CONTENT changed rather than the option being new.
TOKEN = 'v1'

settings = {}


def onSettingsChanged(linkage, newSettings):
    global settings
    settings = newSettings


def template():
    s = settings
    return {
        'modDisplayName': 'Highlights',
        'settingsVersion': 1,
        'column1': [
            templates.createLabel('Marked as new'),

            # markNew returns the control it was given, so it wraps a builder inline
            templates.markNew(templates.createCheckbox(
                'A new switch', 'fresh', s.get('fresh', False),
                tooltip='{HEADER}New{/HEADER}{BODY}Click the row and the flare goes for '
                        'good.{/BODY}')),

            templates.markNew(templates.createSlider(
                'A new slider', 'amount', s.get('amount', 50), 0, 100, 5)),

            # With a token the highlight is repeatable. Change the token to any new
            # string and this one lights up again, even for someone who dismissed it.
            templates.markNew(templates.createDropdown(
                'Changed contents', 'mode',
                templates.generateOptions(['Off', 'Simple', 'Detailed']),
                s.get('mode', 0),
                tooltip='{HEADER}Updated{/HEADER}{BODY}This one carries a token, so it '
                        'can be announced again later.{/BODY}'),
                token=TOKEN),

            templates.createLabel('Not marked'),
            templates.createCheckbox('An ordinary switch', 'plain', s.get('plain', True)),
        ],
        'column2': [
            templates.createLabel('Try it'),
            templates.createActionButton(
                'relight', buttonText='Light them up', label='All three flares',
                tooltip='{HEADER}Light them up{/HEADER}{BODY}Forgets that you have seen '
                        'them, which is what a returning user sees after an '
                        'update.{/BODY}'),
            templates.createActionButton(
                'seen', buttonText='Mark as seen', label='Clear every flare',
                tooltip='{HEADER}Mark as seen{/HEADER}{BODY}The same thing the counter\'s '
                        'own context menu does.{/BODY}'),
            templates.createActionButton(
                'bump', buttonText='Bump the token', label='Only the third one',
                tooltip='{HEADER}Bump the token{/HEADER}{BODY}Re-announces just the '
                        'control whose contents changed.{/BODY}'),
        ],
    }


def onButtonClicked(linkage, varName, value):
    if linkage != LINKAGE:
        return

    if varName == 'relight':
        # Clears the record of what this mod's user has already dismissed. Omit the
        # third argument to clear the lot, or pass a list of varNames to pick.
        g_modsSettingsApi.resetFeatureHighlights(LINKAGE)

    elif varName == 'seen':
        g_modsSettingsApi.markAllFeaturesSeen(LINKAGE)

    elif varName == 'bump':
        global TOKEN
        TOKEN = 'v%d' % (int(TOKEN[1:]) + 1)
        # A token is only compared against what the user last dismissed, so the control
        # needs no reset call of its own. The new token is enough.
        g_modsSettingsApi.resetFeatureHighlights(LINKAGE, ['mode'])

    # Highlights are decided while the panel is being built, so the window has to draw
    # this mod again before anything changes. Without this you would have to close the
    # window and open it once more.
    g_modsSettingsApi.reloadModTemplate(LINKAGE, template())


def init():
    global settings
    settings = g_modsSettingsApi.setModTemplate(
        LINKAGE, template(), onSettingsChanged, onButtonClicked)

    # DEMO ONLY, and a real mod must never do this. Registering for the first time
    # marks every flagged option as already seen, so a fresh install does not greet
    # anyone with a wall of flares. That is the right behaviour and it also means
    # this example would show nothing at all on first run. Clearing the record here
    # puts the window in the state a returning user sees after an update, so the
    # flares and the counter are there to look at the moment the menu opens.
    g_modsSettingsApi.resetFeatureHighlights(LINKAGE)
