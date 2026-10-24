# Mod Menu 2.0.00 - 2.0.17

Release notes of the versions for the game before 2.4.1.0, newest first.

## 2.0.17 (19-09-2026)

**Changed**

- A setting value a mod hands the menu that cannot be saved no longer stops the menu from saving everything else. Only that value is left out, and the log names the mod and the setting.

**Fixed**

- Smaller text written next to larger text on one line, such as a unit beside a value, now sits on the same line as the larger text instead of slightly below it.

## 2.0.16 (18-09-2026)

**Added**

- A control can carry several buttons side by side, for example an up and a down arrow, each with its own tooltip and its own answer to a right click.
- Rows a mod reorders slide to their new places instead of jumping.

**Changed**

- Button icons keep their own colors instead of being toned to grey.
- Switches have a new look, a thin track with a knob that slides across when clicked.

**Fixed**

- Tabs no longer shift sideways when you switch between them.
- The font chosen in the menu settings now applies to the whole window, tabs and text fields included.
- Color options no longer show up as unsaved changes after a mod redraws its options.
- A change not yet applied is no longer lost when a mod redraws its options, for example after a line is moved.

## 2.0.15 (16-09-2026)

**Fixed**

- A short tooltip no longer shows a scrollbar that hides its last line.
- A tooltip taller than the screen always shows its scrollbar and scrolls with the mouse wheel.
- Wrapped text in the right column of a tooltip table lines up correctly.

## 2.0.14 (15-09-2026)

**Fixed**

- An error in another mod can no longer break the menu window, the garage button or the hotkey that opens the menu.
- After a very long tooltip, the tooltips shown next no longer keep its height.
- The settings window uses less of the game's resources while it stays open.

## 2.0.13 (13-09-2026)

**Fixed**

- Scrolling with the mouse wheel now works the same way in every list in the menu.
- The window list opened from the garage button has a scrollbar.

**Changed**

- The window list uses the full height of the screen before it starts to scroll.
- The window list closes when the screen resolution or the interface scale changes.

## 2.0.12 (11-09-2026)

**Fixed**

- After a battle started while the Mod Menu window was open, ESC, the key that opens the menu and the garage button all stopped working in the garage afterwards. The game closes the window on its own when a battle starts, and the menu did not notice, so it kept acting as if the window were still there.

## 2.0.11 (10-09-2026)

**Changed**

- On an ultrawide screen the window no longer stretches across the whole width. It keeps the width it would have on a 16:9 screen of the same height and sits in the middle. On any other screen nothing changes, including a 16:9 screen with the game running in a window.

**Added**

- Wide screen in the menu settings: the window can sit in the middle, against the left or the right edge, or stretch across the whole width as before. Left and right are meant for three monitors joined into one, where the window lands on an outer monitor with the margins a single monitor would show.
- `setWindowDefaults` takes `wideScreen`, so a container can choose where its window starts: `center`, `left`, `right` or `stretch`.
- With debug on, the log records the size and shape of the game's surface when the window opens and whenever it changes.

## 2.0.10 (09-09-2026)

**Fixed**

- A mod switched off and then reset kept its name grayed out in the list on the left, while the switch in its panel already read on. Resetting a mod puts its own on and off state back along with everything else, and the row in the list now follows it. The two other ways of switching a mod, the dot on the row and the switch in the panel, were never affected.

## 2.0.09 (09-09-2026)

**Added**

- A new option carries the word NEW beside its label, in the menu language.
- Picking a mod from the window list plays the sound the game's own controls press with. It was silent before, and on the login screen it reached for a sound that screen does not carry.
- `createHotkey` honors its `float` argument in this edition. `below` gives the keys a line of their own under the label, against the left edge; `right` does the same against the right edge; `none` stays the ordinary row. The argument was accepted and had no effect here until now. The Flash edition draws `right` differently: there the label flows around the keys, which this engine cannot do.
- A container can choose how the hovered row is marked: `bar`, `rules` or `label`.

**Changed**

- The highlight on a new option was a flat fill with a bar at its left, the same as a selected mod in the list. It is a gradient in the accent color now, fading out at every edge, with a breathing bar and a light crossing the row.
- Its colors follow the accent the player picked. They were fixed to the default gold.
- The counter beside the mod's name breathes and sends out a ring.
- The hovered row is marked at its edge instead of by recoloring its label, so the mark stays readable whatever the accent is.
- The hover tint lifts by a fixed step away from the window background rather than by a share of it, so it stays visible on a dark window.
- The log is quiet. A release writes one line saying which version is running, plus anything that actually went wrong. The diagnostics that used to sit beside them are still there and still off: put `"debug": true` in `mods/configs/aslainMenu.json` to get them back.
- The footer button's icon tile takes the window background, so the button carries both of a container's colors instead of only its accent.

**Fixed**

- A value seeded with `setWindowDefaults` stopped being a default the first time the player saved anything in the settings panel. The panel writes every value it holds on each save, so one change claimed the accent, the background, the scale and the font as choices. A value equal to the seed is not stored now.
- The Default button beside the accent and the one beside the background reset to the menu's color, ignoring a color seeded with `setWindowDefaults`. They reset to the container's default now.
- Reset in the settings panel left both colors where they were for a window with no container behind it.
- The footer button took the menu's colors even where a container declared its own. Where one container is in play, the button carries that container's pair.
- The footer button repainted only on Reset. Every color change reaches it now.
- Cancel, the close cross and ESC left a color picked in the panel applied and saved. They put the window's look back to what it was on open.
- A reload that kept the layout brought a highlight back without the NEW tag: the panel is not rebuilt in that case, and only the renderer built the tag.
- A template reload that omitted `enabled` switched the mod off in the list while the panel's own switch still read on.
- `reloadModTemplate` did not store the template it announced, so a highlight marked as seen after a token bump stayed lit until the window was reopened.
- Neither glow animated: the engine refuses `var()` in a keyframe and refuses two units for one property. The shadow is set in the rule and the frames carry the opacity.
- The rows in the settings panel stood too close together, and the row holding the key that opens the menu touched the rows around it. That row takes the height it needs now.
- On the login screen the window list opened away from the button that opens it, and the pointer beneath it aimed at nothing. Both follow the button now, on either screen.
- The window list kept its old width after a resolution change.

**Documentation**

- `registerStyle`: the properties that survive the filter, how selectors are rewritten, what is refused, and the class names to aim at.
- Text fields, the fixed palette (`presets`, `presetsOnly`, `enableAlpha`), the collapsed image, `buttonHandler` and `float` were accepted by the API and documented nowhere. They are written up now.
- See `docs/api.md`.

## 2.0.08 (06-09-2026)

**Changed**

- Auto now shares the options area equally between the columns a mod declares: two take half each, three a third each, four a quarter each. A mod declaring one column keeps half the row. Before this every column in auto was held to a quarter, so a two-column mod stood in the left half with the rest of the row empty.

**Fixed**

- In two and four columns, a mod with fewer columns than the mode asks for took the whole options area, so its rows stretched from edge to edge and a hotkey's keys landed in the far corner. It keeps its share of the row now, the rest stays empty.
- A tab marked full width did not span the panel in auto mode.
- The panel scale could be raised past what the screen holds, and the buttons in the window header fell off the right edge. It stops where the header still fits them, on a 1280 wide screen at 160 per cent. The stored setting is not changed, so a higher one applies again on a wider screen.
- The settings panel kept the size it was opened at until it was closed and opened again, while the font size beside it changed the panel at once. It follows the panel scale now and stays under the button it hangs from.
- Resetting a mod to its defaults was written to the log at a level this game client does not record.
- A mod whose template declares a hotkey as a nested list, `[[262]]`, was handed that shape back on its first apply and could fail on it; the value is stored flat from the start now, the shape the window writes on every save.

**Added**

- A click on the number between the minus and the plus of panel scale, font size or transparency puts that one setting back to its default. A container that seeded its own value through `setWindowDefaults` gets that value, not the menu's.

## 2.0.07 (05-09-2026)

**Added**

- Auto, a third setting under Option columns: each mod is laid out in the columns its own template declares, so a two-column mod fills two columns and leaves the rest of the row empty. Two columns remains the default.

**Fixed**

- Resetting a mod to its defaults reported an unsaved change for every hotkey it has, with the same key shown on both sides of it.
- The lettering in the hotkey chips and in the segmented controls was not centred.
- Colour values were hard to read. They are shown at the size and weight of a hotkey chip now, without the leading hash and in capitals.
- Tooltips along the top edge of the window jumped from one side of the pointer to the other on a small movement. They stay on the left.
- The list of unsaved changes wrapped its labels over several lines while the screen had room beside it. It takes the width it needs, up to the room there is.
- The question asked before resetting a mod did not say which mod it was about.
- Text outgrew its controls as the font size went up: values left their fields, inputs clipped their letters and the rows of the settings panel stopped lining up. Controls grow with the font now.
- After a change of font size, dropdowns that size themselves and pictures fitted to their column opened at the wrong size and corrected themselves on screen a moment later.
- In Auto mode, changing the panel scale left the columns at their previous width until the window was rebuilt.
- A control beside a label that wraps was centred on the whole paragraph. It sits on the first line now, with the info marker beside it, and the wrapped lines go below.
- The colour of a checkbox with colour showed at full strength while its switch was off. It fades with the switch.

**For mod authors**

`setWindowDefaults` now also takes `columns` (`auto`, `two` or `four`), `font` and `fontScale`, so a private container can seed every row of the settings panel except the menu language and the key that opens the window.

## 2.0.06 (03-09-2026)

**Fixed**

- Lists opened inside the window, the language and font pickers and a mod's own dropdowns, landed at the wrong height when Panel scale was set to anything other than 100%.
- A list taller than the screen ran off it. It now stops at the screen edge and scrolls.
- Stepping Panel scale or Font size left such a list open and out of place. It closes on the step now.

## 2.0.05 (03-09-2026)

**Fixed**

- The list of mods under the garage button opened stretched to the full height of the screen when Panel scale was set to anything other than 100%. Panel scale applies to the window only now, and that list follows the game's interface scale.

## 2.0.04 (03-09-2026)

**2.0.04 - the lists of mods explain their rows.**

A mod's own explanation of its entry was never shown. Every mod that registers a window passes one, and the flash mods list has always drawn it on hover, but this window dropped the text on its way in, so hovering a row gave nothing. All three lists show it now: the one from the button in the garage, the one in the title bar, and an author's own submenu. It waits as long as the flash list does, and stays on one side of the pointer instead of flipping across it near the edge of the screen.

**For mod authors**

Nothing to change. The text comes from the `description` you already pass to `addModification`, and a later `updateModification(description=...)` is picked up live. It understands the game's `{HEADER}`, `{BODY}`, `{NOTE}` and `{ATTENTION}` markup, and plain text is wrapped for you.

## 2.0.03 (02-09-2026)

**Fixed**
- **The window opens when the game folder has a non-ASCII character in its path**: any accent, Cyrillic or other non-English letter anywhere in the path stopped the window from opening at all, on every attempt. Thanks to MegaJani for the log.

## 2.0.02 (02-09-2026)

**Fixed**
- **Icons show on every row of the window list**: a row whose icon is a loose file in the game folder came through blank, whatever its author did. Rows whose icon lives in the game's resources were never affected.
- **A row without an icon** gets a small drawn mark instead of a bare grey disc.

## 2.0.01 (02-09-2026)

**Fixed**
- **The window opens for every mod**: a mod passing something other than text as a control's label stopped the window from opening at all. Such values are now left as they are. Thanks to OldSkool for the report.

## 2.0.00 (01-09-2026)

**2.0.00, the first release of Mod Menu.**

One window in the garage for the settings of the mods that use it, instead of each one hiding a panel of its own. Open it from the button beside the gear, or press CTRL and P.

Built for Gameface, the interface layer the game itself moved to. The Flash menu could not be carried across, since the two share no language, no runtime and no drawing model, so the window, the controls and the layout behind them were written for this engine. What was carried over deliberately is the API: a mod written years ago registers and runs here without a line changed.

**Finding things.** The mods are listed down one side and the options of the one you picked fill the rest. Type part of a name to narrow the list as you go, or turn on the letter index and jump straight to a letter. A mod can be switched off from its row without opening it.

**Room to work.** A mod with many settings splits them across tabs, and options run in two columns or four. Where a mod offers pictures you see them, so an icon or a style is chosen by looking rather than by reading its name. Hovering an option explains what it does, in the player's own language wherever the mod supplies the translation.

**Nothing is written until you say so.** Change several mods, apply without closing, and open the full list of what you changed before committing it, old value beside new. Step back through changes one at a time, or cancel everything since the last apply. Each mod has its own reset that restores its author's defaults and touches nothing else.

**New options are announced.** When a mod you already had gains an option, it is marked and counted beside its name, so an update tells you what it brought. The mark clears once you have looked at the option, by clicking its row, resting on it for a moment, or changing it. A newly installed mod never lights up.

**The window is the player's.** Language, font, text size, panel size, accent colour, background, how much of the garage shows through, the letter index, and the key that opens it.

Mods that registered with the older settings menu are taken over as well, so they appear here rather than in a second window.

**Install**

Put `aslain.modmenu_2.0.00.wotmod` in `World_of_Tanks/mods/<game version>/` and remove any older copy from that folder first.

It needs the [OpenWG Gameface](https://gitlab.com/openwg/wot.gameface) loader, version 1.1.6 or newer, which most mod packs already install. Without it the menu says so in `python.log` and no window opens, while everything else keeps working: templates register and values are stored.

**For mod authors**

The [API guide](https://github.com/Aslain/modmenu/blob/main/docs/api.md) covers the paths most mods take, the [full reference](https://github.com/Aslain/modmenu/blob/main/docs/reference.md) lists every builder and every method, and the [examples](https://github.com/Aslain/modmenu/tree/main/examples) are four small mods to copy from.

Gate anything new to this edition on `getVersionTuple() >= (2, 0, 0)` and your mod runs on both editions.
