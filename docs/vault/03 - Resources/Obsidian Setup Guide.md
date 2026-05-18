# Obsidian Setup Guide

> Tags: #obsidian #meta #setup

---

## First-Time Setup

### 1. Open This Vault
- Open Obsidian → **Open folder as vault** → select `D:\SecondBrain`

### 2. Configure Settings (⚙️)

| Setting | Location | Value |
|---|---|---|
| Default new note location | Files & Links | `00 - Inbox` |
| New link format | Files & Links | Relative path |
| Use Wikilinks | Files & Links | ✅ ON |
| Readable line length | Editor | ✅ ON |
| Strict line breaks | Editor | ❌ OFF |
| Spell check | Editor | ✅ ON |

### 3. Set Up Templates
- Settings → Core Plugins → **Templates** → Enable
- Template folder location: `Templates`
- Now use `Ctrl+T` to insert a template into any note

### 4. Set Up Daily Notes
- Settings → Core Plugins → **Daily Notes** → Enable
- Date format: `YYYY-MM-DD`
- New file location: `00 - Inbox/Daily`
- Template: `Templates/Daily Template`
- Now use `Ctrl+D` to create today's note

### 5. Install Community Plugins
- Settings → Community Plugins → Turn OFF restricted mode
- Browse and install:

| Plugin | Purpose | Priority |
|---|---|---|
| **Templater** | Advanced templates with variables | ⭐ Essential |
| **Dataview** | Query notes like a database (powers the Dashboard) | ⭐ Essential |
| **Calendar** | Visual daily notes navigation | ⭐ Essential |
| **Kanban** | Task boards inside Obsidian | Nice to have |
| **Git** | Auto-backup to GitHub | Nice to have |
| **Excalidraw** | Draw diagrams | Nice to have |
| **Advanced Tables** | Tab to navigate tables, auto-format | ⭐ Essential |
| **Outliner** | Better list/bullet handling | Nice to have |

### 6. Configure Templater (after installing)
- Settings → Templater → Template folder: `Templates`
- Enable "Trigger on new file creation"

---

## Keyboard Shortcuts

| Action | Shortcut |
|---|---|
| New note | `Ctrl+N` |
| Quick switcher (find note) | `Ctrl+O` |
| Command palette | `Ctrl+P` |
| Search vault | `Ctrl+Shift+F` |
| Daily note | `Ctrl+D` |
| Insert template | `Ctrl+T` |
| Toggle edit/preview | `Ctrl+E` |
| Graph view | `Ctrl+G` |
| Back | `Alt+←` |
| Forward | `Alt+→` |
| Bold | `Ctrl+B` |
| Link | `Ctrl+K` |
| Checklist | `Ctrl+L` |

---

## Workflow

```
                    ┌──────────────┐
  New idea? ──────→ │  00 - Inbox  │
                    └──────┬───────┘
                           │ Process weekly
                    ┌──────┴───────┐
          ┌─────────┤   Classify   ├─────────┐
          │         └──────────────┘         │
          ▼                ▼                 ▼
  ┌──────────────┐ ┌─────────────┐  ┌──────────────┐
  │ 01-Projects  │ │  02-Areas   │  │ 03-Resources │
  │              │ │             │  │              │
  │ Active work  │ │ Ongoing     │  │ Reference    │
  │ with end date│ │ no end date │  │ material     │
  └──────────────┘ └─────────────┘  └──────────────┘
          │
          │ When done
          ▼
  ┌──────────────┐
  │ 04 - Archive │
  └──────────────┘
```

### Daily Flow
1. `Ctrl+D` → Create daily note
2. Fill in **Focus Today** tasks
3. Throughout the day: dump notes, bugs, ideas
4. End of day: review section
5. Link everything with `[[wikilinks]]`

### Weekly Review
1. Process `00 - Inbox` — move notes to proper folders
2. Review `01 - Projects` — update status, check tasks
3. Update [[Home]] dashboard if needed

---

## Tips

> [!TIP] Link Aggressively
> Every time you mention a concept, wrap it in `[[]]`. Over time you'll build a dense knowledge graph. Check Graph View to see it.

> [!TIP] Don't Organize Upfront
> Dump everything in Inbox. Organize during weekly review. Linking matters more than folders.

> [!TIP] Use Tags + Dataview
> Tag notes with `#debug`, `#learning`, `#adr`, etc. Then use Dataview queries to surface them automatically (like the Dashboard does).

> [!TIP] Templates Save Time
> `Ctrl+T` → pick a template. Every bug gets the Debug Template. Every decision gets the ADR Template. Consistency compounds.
