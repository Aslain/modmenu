# Release notes template

The shape of a release description. The version and one sentence saying what the build is
at the top, then a paragraph per change: what was wrong, why, and what it does now. No
lists of commits.

---

**0.0.0 - one sentence saying what this build is.**

An open dropdown used to close the moment the wheel turned, even on a panel that could
not scroll at all. The list travels with its row now and only closes once the row itself
has left the panel.

The number beside a slider moved as you dragged it. The font gives its digits different
widths at semibold, so the text changed width with the value. It is drawn at regular
weight now, where every digit is the same width.

**Known issues**

Something we know about and have not fixed. Say what triggers it and what to do instead.

**For mod authors**

Only when something changed for them. Say what to check and what to change, and mark
anything optional as optional.

---

## The file

Every release carries `aslain.modmenu_<version>.wotmod`. Tell players to delete the older
copy from `mods/<game version>/` before dropping the new one in, because the game loads
both if they are both there.
