# Release notes template

Cold information. One line per change: what was fixed or added, and the condition it
happened under. No background, no account of how it was found, no names, no thanks.

Only what CHANGED. A section saying nothing changed, or that some part behaves as it
did, is not a release note - drop the section instead of writing it.

---

**Fixed**

- The symptom as a player sees it, and when it happened. Then what it does now.

**Added**

- What the build gained, in one sentence.

**For mod authors**

Only when a mod author has to do something. Say what to change. If there is nothing,
the section does not appear.

---

## The file

Every release carries `aslain.modmenu_<version>.wotmod`. Tell players to delete the older
copy from `mods/<game version>/` before dropping the new one in, because the game loads
both if they are both there.
