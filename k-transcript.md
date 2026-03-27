---
name: k-transcript
description: Extract a Krishnamurti YouTube transcript from the currently open Safari tab, curate key quotes by theme, and append them to the wiki theme files.
user-invocable: true
---

Extract a K transcript from the currently open Safari tab and add curated quotes to the wiki theme files.

## Steps

### 1 — Get title and URL from Safari

```bash
~/workspace/claude_for_mac_local/tools/safari_control.sh current-title
~/workspace/claude_for_mac_local/tools/safari_control.sh current-url
```

Sanitize the title for use as a filename:
- Strip " - YouTube" suffix
- Replace spaces and special characters with underscores
- Keep it readable (max ~80 chars)

### 2 — Extract transcript text

```bash
~/workspace/claude_for_mac_local/tools/safari_read.sh text
```

Parse out only the spoken lines using this awk pattern (strips timestamps):

```bash
awk '
/Search transcript/{found=1; next}
found && /^[0-9]+:[0-9]+[0-9]+ (minute|second|hour)/{
    line=$0
    gsub(/^[0-9]+:[0-9]+ ?[0-9]* ?(minute|hour)[s]?(, [0-9]+ second[s]?)?/, "", line)
    gsub(/^[0-9]+:[0-9]+ ?[0-9]* ?second[s]?/, "", line)
    if (length(line) > 3) print line
}
'
```

### 3 — Save the raw transcript

Save to: `/Users/debaditya/workspace/K-mirror/transcript_<SANITIZED_TITLE>.txt`

### 4 — Curate quotes by theme

Read the transcript carefully. Extract 15–25 of the most potent quotes — lines that carry genuine K insight, not preamble or logistics.

Organize under these themes (add new themes if the talk introduces new territory):

- **On Thought** — thought as memory, knowledge, material process
- **On Relationship** — images, conflict, two parallel lines
- **On Desire** — sensation → image → desire chain
- **On Fear** — structure, time, the undiscovered fears
- **On Observation vs Analysis** — the analyser is the analysed, pure observation
- **On Consciousness & Identity** — common ground, the illusion of the separate self
- **On Memory & Identity** — the ego as memory, the known
- **On Attachment** — corruption, loneliness underneath
- **On Death & Living** — dying to the known while still alive
- **On the Controller & Controlled** — thinker is the thought, no division
- **On Meditation & Systems** — no practice, clarity of free perception
- **On Attention & the Senses** — full attention, no centre
- **On Religion & Freedom** — factual mind, free of thought's inventions
- **On Love** — not knowledge, not remembrance, not desire
- **On the Mirror** — K's own framing of his role

### 5 — Append to wiki theme files

For each theme with quotes, append to the corresponding file in `wiki/` (e.g., `wiki/becoming.md`, `wiki/desire.md`):

```markdown
> "quote one"

> "quote two"

> "quote three"
```

Append to the end of the theme file, before the closing metadata if present. Each theme file is named after the psychological principle (becoming.md, desire.md, observation.md, etc.).

**Important:** Always include source attribution in git commit message: `*(from <Full YouTube Title> — YT:<video_id>)*`

### 7 — Confirm

Report back:
- Video title
- Number of transcript lines extracted
- Number of quotes added
- Themes covered
