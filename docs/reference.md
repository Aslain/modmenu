# Full reference

Every public control builder and every API method, in one place. The [API guide](api.md) walks through the paths most mods take and is the better place to start. This page exists so that nothing is discoverable only by reading code you cannot read.

Two imports carry everything:

```python
from gui.aslainMenu import g_modsSettingsApi, templates
```

Anything not listed here belongs to the window's own machinery. It may exist on the object, and it may disappear without notice.

## Reading this page

Every builder returns a plain dictionary. A template is a dictionary of two lists of them, so anything here can be built, stored and passed around like any other data.

`varName` is the key a control's value arrives under in your callback. `linkage` identifies your mod and must stay stable across versions, since it is also the key your saved values live under.

## Controls

| Builder | What it is |
| --- | --- |
| `createCheckbox(text, varName, value, ...)` | On and off |
| `createDropdown(text, varName, options, value, ..., width, fullWidth)` | One choice from a list |
| `createRadioButtonGroup(text, varName, options, value, ..., inline)` | One choice, all visible at once |
| `createSlider(text, varName, value, min, max, interval, format, ..., width)` | A number on a track |
| `createStepSlider(text, varName, options, value, format, ..., width)` | A track with named stops rather than a range |
| `createRangeSlider(text, varName, value, min, max, interval, step, minRange, labelStep, labelPostfix, ...)` | Two handles, a span. `value` is a pair |
| `createNumericStepper(text, varName, value, min, max, interval, ..., manual)` | A number with plus and minus. `manual=True` lets it be typed |
| `createInput(text, varName, value, ..., width)` | A text field |
| `createHotkey(text, varName, value, ..., float)` | A key combination |
| `createColorChoice(text, varName, value, ..., presets, presetsOnly, enableAlpha)` | A colour |
| `createCheckboxColor(text, varName, value, color, ...)` | A colour with its own on and off. The value is a dict of `enabled` and `color` |
| `createLabel(text, tooltip, tooltipIcon, useHTML)` | Text, no value |
| `createImage(source, width, height, ..., align, valign, containerWidth, containerHeight, collapsed, label, labelAlign, atlas, autoFit)` | A picture in the panel |
| `createEmpty(height)` | Vertical space. Defaults to 20 |
| `createButton(width, height, text, offsetTop, offsetLeft, icon, iconOffsetTop, iconOffsetLeft)` | A button attached to another control, passed as its `button` argument |
| `createActionButton(varName, buttonText, label, icon, width, ...)` | A button standing on its own row |

Every control builder takes `tooltip`, `tooltipIcon` and `useHTML`. A control with a tooltip gets an information mark next to its label.

### Lower level builders

These are what the ones above are made of. Reach for them only to build a control type by hand, passing a value from `COMPONENT_TYPE`.

| Builder | What it is |
| --- | --- |
| `createBase(type, text, ...)` | A component with no value |
| `createControl(type, text, varName, value, ...)` | A component with a value |
| `createOptionsControl(type, text, varName, options, value, ..., inline)` | A component with a value and a list of options |
| `createStepper(type, text, varName, value, min, max, interval, ...)` | Slider, numeric stepper and range slider share this one |

`COMPONENT_TYPE` carries: `EMPTY`, `LABEL`, `CHECKBOX`, `RADIO_BUTTON_GROUP`, `DROPDOWN`, `SLIDER`, `STEP_SLIDER`, `TEXT_INPUT`, `NUMERIC_STEPPER`, `HOTKEY`, `COLOR_CHOICE`, `CHECKBOX_COLOR`, `RANGE_SLIDER`, `IMAGE`, `BUTTON`.

## Options, groups and conditions

| Builder | What it does |
| --- | --- |
| `generateOptions(entries)` | Builds the `options` list for dropdowns and radio groups. Accepts plain strings, pairs of label and tooltip, or dicts |
| `createControlsGroup(master, children, indent=True)` | Children are greyed out while a boolean master is off, and indented under it |
| `enableWhen(control, masterVarName, value, indent, condition)` | Greys the control out unless the master's value satisfies the condition |
| `visibleWhen(control, masterVarName, value, indent, condition)` | Same test, but the control is hidden and the panel closes the gap |
| `enableWhenAll(control, conditions, indent)` | Every condition must hold |
| `enableWhenAny(control, conditions, indent)` | Any one is enough |
| `visibleWhenAll(control, conditions, indent)` | Every condition must hold |
| `visibleWhenAny(control, conditions, indent)` | Any one is enough |
| `createTab(text, components, useFullWidth=False)` | Puts components on a tab. Two tabs are the minimum before the strip appears |
| `markNew(control, token=None)` | Highlights the control as new. See below |
| `escape(text)` | Escapes `&`, `<` and `>` so literal text survives an HTML label |

`CONDITION` carries `EQUAL`, `NOT_EQUAL`, `GREATER`, `GREATER_EQUAL`, `LESS`, `LESS_EQUAL`.

Labels render as HTML, so a literal `<` swallows the rest of the label. `templates.createSlider(escape('master <= 5'), ...)`.

## Highlighting new options

`markNew(control, token=None)` puts a flare on a control's row and a counter next to your mod's name in the list, the way the game marks new options in its own settings.

The highlight clears permanently the moment the user clicks the row or changes the value, and the API remembers that per user. A mod installed for the very first time never lights up, so a new user is not greeted by a wall of flares. Pass a `token` to be able to re-light the same control later: bumping the token counts as a new announcement.

| Method | What it does |
| --- | --- |
| `markFeatureSeen(linkage, varName)` | Clears one highlight, as if the user had visited it |
| `markAllFeaturesSeen(linkage)` | Clears every highlight of your mod at once |
| `resetFeatureHighlights(linkage, varNames=None)` | Lights them up again. For re-announcing on your own terms, such as leaving beta |

## Registering and values

| Method | What it does |
| --- | --- |
| `setModTemplate(linkage, template, callback, buttonHandler=None, multiColumnTemplate=None)` | Registers your mod and returns its saved settings right away |
| `registerCallback(linkage, callback, buttonHandler=None)` | Adds a callback to an already registered mod |
| `getModSettings(linkage, template)` | The saved values for a template, without registering |
| `updateModSettings(linkage, newSettings)` | Writes values from your side. The window follows if it is open |
| `reloadModTemplate(linkage, template, multiColumnTemplate=None)` | Replaces your panel in the open window, for example after a language change |
| `setModDefaults(linkage, defaults)` | Declares your factory defaults explicitly instead of letting them be derived from the template. These are what the reset button restores |
| `resetModToDefaults(linkage)` | Resets your controls live. Uncommitted, so Cancel still reverts it |
| `getModData(linkage, version, default)` | Storage of your own, beside the settings |
| `saveModData(linkage, version, data)` | Writes that storage |
| `setModCollapsed(linkage, collapsed)` | Does nothing here, kept so old code runs. This window shows one mod at a time |

## Live changes

| Method | What it does |
| --- | --- |
| `registerLiveSettingsChange(linkage, callback, fullsettings=True, mode=None)` | Called while the user is still moving a control, before Apply |
| `unregisterLiveSettingsChange(linkage, callback)` | Stops that |
| `notifyLiveSettingsChange(linkage, settings)` | Pushes a live change from your side |

## Images and previews

| Method | What it does |
| --- | --- |
| `updateImage(linkage, varName, source, width, height, removeImage=False, label=None)` | Replaces a picture while the window is open |
| `updateImageAtlas(linkage, varName, atlasSource, frameWidth, frameHeight, columns, count, fps, loop=True, width, height)` | An animated picture from a sprite sheet |
| `replayLiveImages()` | Re-sends the last picture for every live preview. The window calls this itself after a rebuild |
| `registerInputPreview(linkage, varName, handler)` | Offers a live preview of what a text field becomes once your mod has converted it |
| `unregisterInputPreview(linkage, varName)` | Drops that provider |
| `hasInputPreview(linkage, varName)` | Whether one is registered |
| `setInputPreview(linkage, varName, content, token=None)` | Answers a preview request. Accepts the same markup as a label |

## Colours

| Method | What it does |
| --- | --- |
| `getUserColorPresets()` | The user's palette, 48 slots, each a six digit hex string or `None` |
| `setUserColorPresets(presets)` | Writes it |
| `getColorValueDefault(linkage, varName)` | The default colour of one control |
| `requestColorValueReset(linkage, varName)` | Pushes that default back into the open window |
| `userPresetAction(action, slot)` | Relays a palette context menu pick |

## Languages

| Method | What it does |
| --- | --- |
| `registerLanguages(linkage, codes)` | Declares which languages your mod ships, so the menu only offers ones something can display |
| `getRegisteredLanguages()` | Every code any mod declared |
| `getMenuLanguage()` | The language the menu is showing right now. A mod set to follow the menu should read this, not the client language |
| `getMenuLanguageSetting()` | What the player picked, or `auto` |
| `setMenuLanguage(code)` | Switches it and tells every mod through `onMenuLanguageChanged` |
| `registerModTranslation(linkage, mapping)` | Translates your labels for display only. Saved values are untouched, so nothing resets |

## Your mod's look in the window

| Method | What it does |
| --- | --- |
| `registerIcon(linkage, source)` | An icon beside your mod in the list and in its header. `None` removes it |
| `registerStyle(linkage, css)` | Restyles your own section. Only colour properties survive and every selector is scoped to your panel |
| `getModIcons()` | Every registered icon |
| `getModStyles()` | Every registered style |

## The window itself

Branding and look are honoured only on a private API instance, meaning a mod that builds its own object with its own settings file and opens the view with it. On the shared instance they are ignored, since one mod does not get to rename the window everybody shares.

| Method | What it does |
| --- | --- |
| `setWindowBranding(title=None, icon=None)` | Names and marks the window, for a container holding one author's mods |
| `getWindowBranding()` | Reads that back |
| `setWindowDefaults(**values)` | A look to fall back on where the user has chosen nothing. Never an override |
| `getWindowDefaults()` | Reads those back |
| `applyWindowSettings(save=False, **values)` | Applies a look right now. Without `save` it lives only until the window closes, so a mod can offer previews without writing anything |
| `revertWindowSettings()` | Drops an unsaved preview and returns to what is stored |
| `getWindowScrollPosition()` / `setWindowScrollPosition(pos)` | Scroll memory, session only |
| `getWindowSelectedMod()` / `setWindowSelectedMod(linkage)` | Which mod was open last, remembered by linkage rather than by row |
| `getMultiColumnMode()` / `setMultiColumnMode(value)` | The two or four column toggle. Persisted |
| `canOpenWindow()` | Whether a window can actually be shown. Everything else works without it, but nothing can be opened to look at |

Look values accepted by `setWindowDefaults` and `applyWindowSettings`: `accent`, `background`, `backgroundAlpha`, `scale`, `transparent`, `fullScreen`, `azMode`.

## The window list

`modsList` offers the same five calls poliroid's `g_modsListApi` does, with identical signatures and no Flash package required: `addModification`, `updateModification`, `removeModification`, `alertModification`, `clearModificationAlert`.

```python
if hasattr(g_modsSettingsApi, 'modsList'):
    g_modsSettingsApi.modsList.addModification(...)
```

## Hotkeys

| Method | What it does |
| --- | --- |
| `getAllHotkeys()` | Every hotkey registered by every mod |
| `checkKeyset(keys)` | Whether a key combination is currently held. `checkKeySet` is the same method under the other spelling |

## Version and identity

| Method | What it does |
| --- | --- |
| `getVersion()` | The version as a string |
| `getVersionTuple()` | The same as a tuple, for comparing. The Gameface edition is `(2, 0, 0)` and above |

## Template helpers

Rarely needed directly, since `setModTemplate` does this for you.

| Method | What it does |
| --- | --- |
| `getSettingsFromTemplate(template)` | The values a template declares |
| `getSettingsFromColumn(column)` | The same for one column |
| `compareTemplates(newTemplate, oldTemplate)` | Whether the structure changed, which is what decides if stored values survive |

## Not for mods

These belong to the window and the storage behind it: `loadSettings`, `loadState`, `saveState`, `clearState`, `generateSettingsData`, and the `onHotkeyStartAccept`, `onHotkeyStopAccept`, `onHotkeyDefault`, `onHotkeyClear` and `onHotkeySet` handlers the window calls while a key is being bound. They are listed so you know what they are when you see them, not so you call them.
