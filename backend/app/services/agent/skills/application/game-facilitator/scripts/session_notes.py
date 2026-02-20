#!/usr/bin/env python3

"""
session_notes.py - Generate session note templates

Creates structured session notes for tracking:
- What happened (summary)
- NPCs introduced
- Locations visited
- Plot threads
- Player decisions
- Next session setup

Usage:
  python scripts/session_notes.py "Session Title"
  python scripts/session_notes.py "Session Title" --output session-3.md
"""

import os
import sys
from datetime import date


def get_date():
    return date.today().isoformat()


def generate_session_notes(title):
    d = get_date()
    return """# {title}

**Date:** {d}
**Duration:** [X hours]
**Players Present:** [List]

---

## Session Summary

[2-3 sentences capturing the key events]

---

## What Happened

### Opening Situation
[What was the state at session start?]

### Key Events
1. [First major thing that happened]
2. [Second major thing]
3. [Third major thing]

### Ending State
[How did the session end? Cliffhanger? Resolution?]

---

## NPCs Encountered

### New NPCs

| Name | Role | Notable |
|------|------|---------|
| [Name] | [What they do] | [What players remember them for] |

### Returning NPCs

| Name | What Happened |
|------|---------------|
| [Name] | [Their role in this session] |

---

## Locations

### New Locations
- **[Location Name]:** [Brief description and what happened there]

### Revisited Locations
- **[Location Name]:** [What changed or was discovered]

---

## Plot Threads

### Advanced
- [ ] [Thread name]: [What progress was made]

### New
- [ ] [New thread]: [How it was introduced]

### Dormant
- [ ] [Thread on hold]: [Why it's waiting]

### Resolved
- [x] [Completed thread]: [How it resolved]

---

## Player Decisions

Significant choices the players made:

1. **[Decision]:** [What they chose and why it matters]
2. **[Decision]:** [What they chose and why it matters]

---

## Consequences Pending

Things that will happen because of this session:

- [ ] [NPC will react to...]
- [ ] [Faction will respond by...]
- [ ] [Environment will change because...]

---

## Loot/Resources

### Acquired
- [Item/resource]: [Where/how obtained]

### Expended
- [Item/resource]: [How used]

---

## Memorable Moments

[Quote, scene, or moment worth remembering]

---

## GM Notes

### What Worked
- [Thing that went well]

### What to Improve
- [Thing to do better]

### Prep for Next Session
- [ ] [Thing to prepare]
- [ ] [NPC to develop]
- [ ] [Location to detail]

---

## Next Session

### Setup
[What situation will open the next session?]

### Threads to Pursue
1. [Most pressing thread]
2. [Secondary thread]

### NPCs Likely to Appear
- [Name]: [Why]

---

*Notes taken: {d}*
""".format(title=title, d=d)


def show_usage():
    print("""
Session Notes Generator
=======================

Generate structured session note templates.

Usage:
  python scripts/session_notes.py "Session Title"
  python scripts/session_notes.py "Session Title" --output file.md

Options:
  --output, -o    Output file path (default: prints to console)
""")


def main():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        show_usage()
        sys.exit(0)

    title = ""
    output = ""

    i = 0
    while i < len(args):
        if args[i] in ("--output", "-o"):
            i += 1
            output = args[i] if i < len(args) else ""
        elif not args[i].startswith("-"):
            title = args[i]
        i += 1

    if not title:
        print("Error: Session title required", file=sys.stderr)
        show_usage()
        sys.exit(1)

    notes = generate_session_notes(title)

    if output:
        os.makedirs(os.path.dirname(output) if os.path.dirname(output) else ".", exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            f.write(notes)
        print("Session notes created: {}".format(output))
    else:
        print(notes)


if __name__ == "__main__":
    main()
