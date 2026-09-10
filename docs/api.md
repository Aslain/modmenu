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
| `createCheckboxColor` | `value`, `color`, and the color arguments above |
| `createLabel` | text only, plus a tooltip |
| `createImage` | `source`, `width`, `height`, `align`, `valign`, `containerWidth`, `containerHeight`, `autoFit`, `label`, `labelAlign`, `atlas` |
| `createActionButton` | `buttonText`, `label`, `icon`, `width`, `height`, `align` |
| `createEmpty` | `height`, for spacing |

`templates.generateOptions(entries)` turns a list of strings into the option dicts the
dropdown and the radio group expect.

Two arguments in that table are worth a sentence. `createNumericStepper(..., manual=True)`
lets the player type the number instead of only stepping to it.

`createHotkey(..., float=)` says where the keys sit when the label is long. The default
`'none'` leaves the row as it is - label left, keys right - which puts the two at
opposite ends of a wide column. `'below'` gives the keys a line of their own under the
label, against the left edge, and `'right'` does the same against the right edge.

The editions differ here, so it is worth knowing which one you are drawing on. In the
Flash edition `'right'` floats the keys and the label flows around them, narrow beside
them on the first line and full width underneath. The Gameface edition cannot do that -
its engine has neither `float` nor `shape-outside`, so text does not flow around
anything - and `'right'` there means the line of its own described above.

### Text fields

```python
templates.createInput('Greeting', 'greeting', 'Hello', width=260, maxLength=40)

templates.createInput(
    'Message of the day', 'motd', '<b>Hello</b><br>and welcome',
    textArea=True, textRows=4, textColumns=60,
    valueIsHTML=True, convertNLtoBR=True,
    monospace=True, span=2,
)
```

`textArea` makes the field multi-line and `textRows` says how many lines of it are
visible. `maxLength` caps the whole value; `textColumns` caps a single LINE of it.
That second one is a count of characters and not a width - markup included, so
`<b>hello</b>` is twelve - because this engine exposes no text geometry to measure
against. Typing past the cap simply does nothing on that line.

`valueIsHTML` says the value your mod stores is markup rather than plain text.
`convertNLtoBR` builds on it: the player sees `<br>` as real line breaks and gets
them back as `<br>` when the value returns to you. The conversion happens only at
that boundary, so what is stored and what your callback receives keep exactly the
shape you gave them. It needs `valueIsHTML=True`, which is how the field knows a
`<br>` in the value is a tag and not something the player typed.

`monospace` renders this one field in a fixed-width font whatever the menu is set
to, for a text area whose columns should line up.

`span` is how many COLUMNS the control takes, counted from its own. It is the only
way to be wider than a column: a width you declare is capped at the column, so a
control can never spill over its neighbour.

### A color picker limited to your own palette

`presets` adds a row of your colors to the picker. `presetsOnly=True` takes away
everything else - the spectrum, the RGB sliders and the hex field - so the player can
pick one of your colors and cannot type a value of their own.

```python
CLASS_COLORS = ['980000', 'C3A500', '467900', '005FA5', '7D28A5']

templates.createColorChoice(
    'Heavy tank color', 'colorHT', '980000',
    presets=CLASS_COLORS,
    presetsOnly=True,
)
```

Up to 24 colors, laid out in rows of twelve, with or without a leading `#`. The same
two arguments work on `createCheckboxColor`. `presets` on its own leaves the full
picker in place and simply offers your colors beside it; `presetsOnly` without
`presets` does nothing, since there would be nothing left to pick from.

`enableAlpha=True` is the other argument worth knowing about here, and it changes the
shape of what you store: the picker gains an alpha channel and the value carries eight
hex digits (`rrggbbaa`) instead of six. A six-digit default is read as fully opaque.
Gameface edition only.

Both `presetsOnly` and `enableAlpha` are newer than the first release of either edition -
Gameface 2.0.0, Flash 1.5.0 - and older builds raise `TypeError` rather than ignoring
them, so gate on the version or catch it:

```python
try:
    control = templates.createColorChoice(
        text, varName, value, presets=CLASS_COLORS, presetsOnly=True)
except TypeError:
    control = templates.createColorChoice(text, varName, value)
```

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

`enableWhen` grays a control out, `visibleWhen` takes it off the panel and closes the gap.
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

### An image slot that starts empty

`createImage(..., collapsed=True)` starts the image as a zero-height slot rather than
reserving the full container, for the case where the default state shows no picture.
Call `updateImage()` with a path to expand it, and `updateImage(..., removeImage=True)`
to collapse it again - the controls below jump up, and `source`, `width` and `height`
are ignored on that call.

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

Buttons have a second route that spares you that check: pass `buttonHandler` to
`setModTemplate` or `registerCallback` and it is called for your own buttons only, the
way `callback` is called for your own settings.

```python
def onButton(linkage, varName, value):
    ...

g_modsSettingsApi.setModTemplate(LINKAGE, template, onSettings, onButton)
```

Buttons have a second route that skips the subscription entirely: pass 
to  or  and it is called for your own buttons only,
the way  is called for your own settings.



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

### Arguments this edition accepts and does not act on

The two editions share one set of template helpers, and a few arguments have no
counterpart in this frontend. They are accepted, passed through and read by nobody: your
mod raises no error and sees no effect. They are listed here because an argument that
fails loudly costs you a minute, and one that fails silently can cost an afternoon.

| Argument | Where | What happens here |
| --- | --- | --- |
| `tooltipIcon` | every control | the tooltip is drawn as text, with no icon |
| `manual` | `createNumericStepper` | the value is always set with the `+` and `-` buttons |
| `step`, `minRange`, `labelStep`, `labelPostfix` | `createRangeSlider` | the slider is drawn from `min`, `max` and `interval` alone: no division marks under the track, no labels beneath them, and no floor on how close the two knobs may come |

Keep passing them if your mod also runs on Flash. They are part of the signatures on
purpose, so one template serves both editions and a mod written for Flash runs here
unchanged.

`float` on `createHotkey` is a different case: both editions act on it, but they draw
`right` differently. See [Controls](#controls).

## Restyling your own section

`registerStyle(linkage, css)` hands the window a stylesheet for one mod. Call it
again to replace it, pass `None` or an empty string to drop it.

```python
api.registerStyle('my.mod', '''
    .mm-comp-label { color: #C8D8E8; }
    .mm-section .mm-comp-label { color: #7BA7D0; }
    .mm-row-name { color: #C8D8E8; }
''')
```

Nothing in that sheet is trusted. It is taken apart, filtered and rewritten before it
reaches the document, so a rule cannot reach outside the mod that registered it.

**Properties that survive.** Color and nothing else: `color`, `background`,
`background-color`, `border-color` and its four sides, `outline-color`, `fill`,
`stroke`, `opacity`. Every other declaration is dropped, so layout, size, spacing and
fonts stay the window's own. A value containing `url(`, `expression(`, `javascript:`,
`@import` or `!important` is dropped too.

**Selectors are rewritten, not obeyed.** A selector naming `mm-row` is scoped to that
mod's row in the list; everything else is scoped to that mod's option panel. So
`.mm-comp-label { ... }` becomes a rule that can only match labels inside your own
panel, however it was written. `html`, `body`, `:root`, `*` and the window's own
furniture (`mm-window`, `mm-header`, `mm-footer`, `mm-sidebar`, `mm-root`,
`mm-backdrop`) are refused outright, as are `@import`, `@media` and `@font-face`.

**Class names worth aiming at.** In the panel: `.mm-comp` is one option's box,
`.mm-comp-label` its label, `.mm-section` a section header, `.mm-switch` a toggle,
`.mm-slider-fill` the filled part of a slider, `.mm-dd` a dropdown, `.mm-input` a text
field, `.mm-key` a hotkey chip. In the list: `.mm-row` your row, `.mm-row-name` its
text, `.mm-row-dot` the dot beside it, `.mm-badge-new` the new-options counter.

**What it cannot reach today.** The menu's own CSS variables. The colors of the
new-option flare live in `--mm-flare-strong`, `--mm-flare-soft`, `--mm-flare-none` and
the three `--mm-sheen-*` beside them, all derived from the accent the player chose, and
a custom property is not one of the properties above, so setting one has no effect.

A word on what this is for. The window has one look, chosen by the player, and a mod
that repaints its whole section fights that choice rather than the menu. It is meant
for a mod with an identity of its own to carry a little of it - a section header in
its color, a label picked out - not for a second theme inside somebody else's window.

## A window of your own

A mod that builds its own API object, with its own settings file, gets a window of its
own: the name on it, the mark beside it and the look of it are yours to set. On the
shared instance these calls are ignored, since one mod does not get to restyle the
window everybody shares.

```python
api.setWindowBranding(title='My mods', icon='gui/maps/icons/mymods/icon.png')
api.setWindowDefaults(accent='7B4FA8', background='171A1D', columns='two')
```

In `auto` a mod is laid out in the columns its own template declares, and they share
the options area equally: two columns take half each, three a third each, four a
quarter each. A template declaring one column takes half the row.

`setWindowDefaults` is a starting point, never an override. A player who picks their
own accent or column layout keeps it, and the Reset in the settings panel lands on
your values rather than the menu's. Call it whenever you like, including while the
window is open, and the panel follows at once.

It takes `accent`, `background`, `backgroundAlpha`, `scale`, `transparent`,
`fullScreen`, `azMode`, `columns` (`auto`, `two` or `four`), `font`, `fontScale`,
`rowHighlight` and `wideScreen`.

`rowHighlight` is how the row under the pointer is marked in the window list:

| Value | Drawn as |
| --- | --- |
| `bar` | A bar down the row's left edge. The default, and the same mark a selected mod carries in the list |
| `rules` | A line above and below the row |
| `label` | The label itself takes the accent, and nothing else marks the row |

`label` is what the menu drew before 2.0.09 and it has a catch worth knowing: the
whole signal is the text color, so it disappears when the accent is close to the
background. The other two keep the label light and mark the row instead.

`wideScreen` is where the window sits on an ultrawide screen:

| Value | Drawn as |
| --- | --- |
| `center` | The default. As wide as the window would be on a 16:9 screen of the same height, in the middle |
| `left` | The same width, against the left edge |
| `right` | The same width, against the right edge |
| `stretch` | 96.5% of the whole width, the way every window was drawn before 2.0.11 |

Short of an ultrawide all four draw the same window, so seeding one changes nothing
there. The window counts a screen as ultrawide from 2.2 to 1: a 16:9 monitor with the
game in a window, or with the taskbar showing, is a little wider than 16:9 and is not
one. The three narrow ones also keep the side margin a 16:9 screen would show, which
puts them exactly on the left, middle or right monitor of three joined into one. Full
screen, when the player turns it on, takes the whole surface regardless.
That is every row of the settings panel except the menu language and the key that
opens the window, which belong to the menu as a whole rather than to one window.

To change a look right now rather than seed one, `applyWindowSettings(save=False,
**values)` paints the open window without writing anything, which is what a preview
button in your own GUI needs, and `revertWindowSettings()` puts back what is stored.

## Translations

```python
g_modsSettingsApi.registerModTranslation(linkage, 'de', {'key': 'text'})
g_modsSettingsApi.registerLanguages(linkage, ['en', 'de', 'pl'])
```

The menu shows the language the player picked in its own settings, and offers only the
languages something can actually display.
