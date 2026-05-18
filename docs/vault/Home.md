# 🏠 Dashboard

> *Agent de Gestion Sociale — Second Brain*

---

## 🚀 Active Projects

| Project | Status | Priority |
|---|---|---|
| [[Agent de Gestion Sociale]] | 🟢 Active | P0 |

---

## 📋 Quick Access

### Core Architecture
- [[Plugin Architecture]]
- [[Config System]]
- [[Core Module Overview]]

### Development
- [[Debug Log]]
- [[Architecture Decisions]]
- [[Dependencies Tracker]]

---

## 📥 Inbox
```dataview
LIST
FROM "00 - Inbox"
SORT file.ctime DESC
LIMIT 10
```

## ✅ Recent Tasks
```dataview
TASK
FROM "01 - Projects"
WHERE !completed
LIMIT 15
```

---

## 📊 Vault Stats

```dataview
TABLE length(rows) AS "Notes"
FROM ""
GROUP BY file.folder
SORT length(rows) DESC
```

---

> [!TIP] Quick Capture
> `Ctrl+N` → write → tag → link with `[[]]` → move later.
