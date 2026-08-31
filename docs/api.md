# API reference

Mod Menu is a new implementation of the API the Flash settings menu used. The interface
is the same, the code behind it is not, so a mod written for that one works here
unchanged. Everything on this page that is new to this edition is marked, and every one
of those is optional.

This page teaches the paths most mods take. For the complete list of builders and
methods, including the corners this one skips, see the [full reference](reference.md).

## Getting hold of it

Ask for this menu first, and fall back to whatever else provides the API:

```python
g_modsSettingsApi = None
templates = None
try:
    # this menu
    from gui.aslainMenu import g_modsSettingsApi, templates
except ImportError:
    try:
        # izeberg's original, the Flash edition, or nothing at all
        from gui.modsSettingsApi import g_modsSettingsApi, templates
    except ImportError:
        pass
```

**The order matters, and the two names are not interchangeable.** `gui.aslainMenu` is
this menu and nothing else. `gui.modsSettingsApi` is whichever package claimed that name
on the player's machine: this one when nothing else did, izeberg's original when another
mod brought it along, or the Flash edition. Asking for this menu first means a player who
has both gets the new window, while a player who has only the old one still gets a
working mod.

Guard both imports. A player with none of them installed should get your mod running on
its own defaults, not a traceback.

An import name and a package file name are separate things, and neither one can be
derived from the other. Import `gui.aslainMenu`. Never build an import out of whatever
the wotmod file happens to be called, even in a release where the two look alike.

The absence of a name is worth trusting as a signal. This menu leaves `gui.modsSettingsApi`
alone when another package owns it, and answers to neither old name when it cannot open a
window at all, which is the case when the Gameface loader is missing. So a mod that has a
mode without a settings window can rely on the import failing to tell it to use that mode.

## Registering

```python
def onSettingsChanged(linkage, newSettings):
    global settings
    settings = newSettings

template = {
    'modDisplayName': 'My Mod',
    'settingsVersion': 1,
    'enabled': True,
    'column1': [...],
    'column2': [...],
}

settings = g_modsSettingsApi.setModTemplate('my.mod', template, onSettingsChanged)
```

`setModTemplate` returns the saved settings straight away, so one call registers the
window and hands you the values to run with.

Keys of the template:

| Key | Meaning |
| --- | --- |
| `modDisplayName` | The name in the mod list |
| `settingsVersion` | Raise it when you change the shape of your settings. The menu then drops what it stored and starts from your new defaults |
| `enabled` | Adds the on and off switch, and the dot in the list |
| `column1`, `column2` | The two columns of controls |
| `multiColumnTemplate` | A second layout used when the player picks four columns |
| `tabs` | A list of `templates.createTab(...)` instead of columns |

## Controls

Every one of these takes `tooltip` and `useHTML`, and most take `button`, a small action
button drawn beside the control.

| Helper | Arguments beyond text and varName |
| --- | --- |
| `createCheckbox` | `value` |
| `createDropdown` | `options`, `value`, `width`, `fullWidth` |
| `createRadioButtonGroup` | `options`, `value`, `inline` |
| `createSlider` | `value`, `min`, `max`, `interval`, `format`, `width` |
| `createStepSlider` | `options`, `value`, `format`, `width` |
| `createRangeSlider` | `value`, `min`, `max`, `interval`, `step`, `minRange`, `labelStep`, `labelPostfix` |
| `createNumericStepper` | `value`, `min`, `max`, `interval`, `manual` |
| `createInput` | `value`, `width`, `textArea`, `textRows`, `textColumns` |
| `createHotkey` | `value`, `float` |
| `createColorChoice` | `value`, `presets`, `presetsOnly`, `enableAlpha` |
| `createCheckboxColor` | `value`, `color`, and the colour arguments above |
| `createLabel` | text only, plus a tooltip |
| `createImage` | `source`, `width`, `height`, `align`, `valign`, `containerWidth`, `containerHeight`, `autoFit`, `label`, `labelAlign`, `atlas` |
| `createActionButton` | `buttonText`, `label`, `icon`, `width`, `height`, `align` |
| `createEmpty` | `height`, for spacing |

`templates.generateOptions(entries)` turns a list of strings into the option dicts the
dropdown and the radio group expect.

## Layout

```python
templates.createTab('Display', [control, control], useFullWidth=False)
templates.createControlsGroup(master, [child, child], indent=True)
templates.enableWhen(control, 'masterVarName', True, indent=True)
templates.visibleWhen(control, 'masterVarName', 5, condition=CONDITION.GREATER)
templates.enableWhenAll(control, conditions)
templates.visibleWhenAny(control, conditions)
templates.markNew(control, token='1.4.0')
```

`enableWhen` greys a control out, `visibleWhen` takes it off the panel and closes the gap.
`markNew` flares the row until the player has seen it, and counts it beside your mod's
name until then.

## Text and tooltips

Labels and tooltips take a small subset of html: `<font color size>`, `<b>`, `<i>`,
`<u>`, `<br>` and `<img src width height vspace hspace>`. Pass `useHTML=False` to have
the text shown exactly as written.

A tooltip can carry blocks:

```
{HEADER}Title{/HEADER}{BODY}What it does{/BODY}
{ATTENTION}A warning worth reading{/ATTENTION}
{ROWS}name : what it means{/ROWS}
```

`{ROWS}` builds a two column table, one row per line, the name and the description
separated by a colon. Tables can sit inside prose, and a tooltip taller than the screen
scrolls under the wheel.

## Value formats, new in this edition

`createSlider` and `createStepSlider` take a `format`. It has always accepted the
`{{value}}` token. This edition also reads a printf conversion when there is no token:

```python
templates.createSlider('Scale', 'scale', 1.0, 0.5, 3.0, 0.05, format='%.2f')
templates.createSlider('Offset', 'offset', 12.3, 0, 30, 0.05, format='%6.2f px')
```

`%.2f` writes 0.8 as `0.80`. `%6.2f px` holds the field at six characters so the unit
never moves as the digits change. `%06.2f` pads with zeros. Widths count the whole field,
the dot and the decimals included, exactly as printf has always counted them. A format
containing `{{value}}` is substituted as before, so nothing written for the Flash edition
changes meaning. The Flash edition prints a printf format literally, so a mod shipping
for both keeps the token there.

## Images

`createImage` reserves the room the picture needs when you pass `autoFit=True`, or holds
a fixed box with `containerWidth` and `containerHeight`. A picture too large for the room
is scaled down and marked with a small badge saying so.

An `<img>` inside a label or a tooltip is drawn at the size you declare, provided you
declare **both** width and height. With one of the two the engine cannot work out the
other and draws the picture at its own size.

For animation, `atlas={'source': ..., 'frameWidth': ..., 'frameHeight': ..., 'columns':
..., 'count': ..., 'fps': ..., 'loop': True}` plays a sprite sheet, and
`updateImageAtlas` swaps it while the window is open.

## Live updates

```python
g_modsSettingsApi.reloadModTemplate(linkage, template)
g_modsSettingsApi.registerLiveSettingsChange(linkage, callback, fullsettings=False)
g_modsSettingsApi.updateImage(linkage, varName, source, width, height)
g_modsSettingsApi.registerInputPreview(linkage, varName, callback)
```

`registerLiveSettingsChange` calls you as the player moves a slider, before Apply.
`registerInputPreview` lets you draw a preview of what a text field would produce, which
is what a mod with its own markup format uses.

## Events

The API carries a set of events you can subscribe to directly. They are plain
attributes, so a mod does not need to subclass anything or call a register method:

```python
def onOpened():
    ...

g_modsSettingsApi.onWindowOpened += onOpened
```

| Event | Fires when |
| --- | --- |
| `onWindowOpened()` | The window has opened |
| `onWindowClosed()` | The window has closed |
| `onSettingsChanged(linkage, settings)` | Any mod's settings were applied. The callback you passed to `setModTemplate` is subscribed to this one for you |
| `onButtonClicked(linkage, varName, value)` | A button in a template was pressed, with `value` as `None` |
| `onMenuLanguageChanged(code)` | The player changed the menu language. Rebuild your template if your labels are translated |
| `onResetMod(linkage, defaults)` | A mod was reset to its defaults from its own header |
| `onReloadMod(linkage, template)` | A mod's template was replaced while the window was open |
| `onHotkeysUpdated()` | A hotkey was rebound |

Check the linkage in handlers that carry one. Every mod's events reach every subscriber,
so a mod acting on another mod's linkage is acting on something that is not its own.

The instance carries further events beyond these. They drive the window's own machinery,
such as image and preview traffic, and are not part of what a mod should rely on.

## Asking whether a window can be opened

The window is a Gameface view, so it needs the OpenWG Gameface loader. Without it
everything else still works, a template registers and your values are stored and handed
back, but nothing can be opened to look at them.

```python
if getattr(g_modsSettingsApi, 'canOpenWindow', lambda: True)():
    ...
```

Ask this if your mod has a mode that does not need a settings window, rather than finding
out by the window never appearing. The check reads the very things the window itself
tests before it opens, so it cannot say yes and then fail. It is absent in the Flash
edition and in izeberg's, hence the `getattr` with a default.

## Telling the two editions apart

```python
tuple(g_modsSettingsApi.getVersionTuple()) >= (2, 0, 0)
```

The Gameface edition reports 2.0.0 and higher, the Flash one stays on 1.x. Gate anything
this page marks as new on that, and your mod runs on both.

The menu itself is released under the same number, written 2.0.00, so its first
release and the contract it answers to are one and the same. That is deliberate: the
Flash edition reports 1.7.1 under a name this menu also answers to, so starting at
1.x here would read as older while being newer.

Compare the tuple, never the string. `getVersionTuple()` gives `(2, 0, 0)` and stays
three numbers whatever the release is called, while `getVersion()` returns the same
text as the package file, padding included.

## Translations

```python
g_modsSettingsApi.registerModTranslation(linkage, 'de', {'key': 'text'})
g_modsSettingsApi.registerLanguages(linkage, ['en', 'de', 'pl'])
```

The menu shows the language the player picked in its own settings, and offers only the
languages something can actually display.
