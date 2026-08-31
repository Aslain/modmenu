# coding: utf-8
""" One of every control, so you can see what each looks like and what it stores.

Every helper also takes tooltip and useHTML, and most take button.
"""
from gui.aslainMenu import g_modsSettingsApi, templates

LINKAGE = 'example.controls'

COLOURS = templates.generateOptions(['Red', 'Green', 'Blue'])

settings = {}


def onSettingsChanged(linkage, newSettings):
    global settings
    settings = newSettings


def template():
    s = settings
    return {
        'modDisplayName': 'Control types',
        'settingsVersion': 1,
        'column1': [
            templates.createLabel('--- Simple ---'),
            templates.createCheckbox('Checkbox', 'check', s.get('check', True)),
            templates.createDropdown('Dropdown', 'drop', COLOURS, s.get('drop', 0)),
            # fullWidth stretches it to the column instead of fitting its widest option
            templates.createDropdown('Dropdown, full width', 'dropWide', COLOURS,
                                     s.get('dropWide', 0), fullWidth=True),
            templates.createRadioButtonGroup('Radio group', 'radio', COLOURS,
                                             s.get('radio', 0), inline=True),
            templates.createInput('Text', 'text', s.get('text', 'hello')),
            templates.createInput('Several lines', 'notes', s.get('notes', ''),
                                  textArea=True, textRows=4),
        ],
        'column2': [
            templates.createLabel('--- Numbers ---'),
            templates.createSlider('Slider', 'slider', s.get('slider', 5), 0, 10, 1),
            # a printf format fixes the decimals and the width of the field
            templates.createSlider('With a format', 'scale', s.get('scale', 1.0),
                                   0.5, 3.0, 0.05, format='%.2f x'),
            templates.createStepSlider('Named steps', 'step',
                                       templates.generateOptions(['Low', 'Mid', 'High']),
                                       s.get('step', 1)),
            templates.createNumericStepper('Stepper', 'num', s.get('num', 10), 0, 100, 1,
                                           manual=True),
            templates.createLabel('--- The rest ---'),
            templates.createColorChoice('Colour', 'colour', s.get('colour', 'E0A248')),
            templates.createCheckboxColor('Checkbox and colour', 'markOn',
                                          s.get('markOn', True), s.get('markColour', 'F23030')),
            templates.createHotkey('Hotkey', 'key', s.get('key', [])),
            templates.createActionButton('doThing', buttonText='Run', label='An action'),
        ],
    }


def init():
    global settings
    settings = g_modsSettingsApi.setModTemplate(LINKAGE, template(), onSettingsChanged)
