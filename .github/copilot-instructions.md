Here's some info sourced from the web to help coding in this repo:

# Slack Canvas API Key Info (from Slack docs)

These are things an offline AI needs to know which are not easily discoverable without internet:

---

## document_content object

- Canvases expose a `document_content` object with two fields:  
  `type` (currently the only supported value is `"markdown"`) and `markdown` (the content). :contentReference[oaicite:0]{index=0}
- Supported markdown elements include (among others):
  - headings (`h1`–`h3`) :contentReference[oaicite:1]{index=1}
  - bold, italic, strikethrough :contentReference[oaicite:2]{index=2}
  - bulleted and ordered lists, checklists :contentReference[oaicite:3]{index=3}
  - tables (with limit ~300 cells) :contentReference[oaicite:4]{index=4}
  - divider / horizontal rule, code block/span :contentReference[oaicite:5]{index=5}
  - file/message/channel/user/profile/website/“unfurl” links :contentReference[oaicite:6]{index=6}

---

## Section lookup via canvases.sections.lookup

- There is an API method `canvases.sections.lookup` that returns **section IDs** inside a canvas by certain criteria. :contentReference[oaicite:7]{index=7}
- Filtering criteria can include:
  - `section_types`: any of `h1`, `h2`, `h3`, or `any_header` :contentReference[oaicite:8]{index=8}
  - `contains_text`: matches sections whose heading text contains a given substring. :contentReference[oaicite:9]{index=9}

---

## Data & Versioning Export Features

- When doing workspace exports (or using Slack’s Discovery or Audit APIs), the export includes:
  - current canvas content :contentReference[oaicite:10]{index=10}
  - version history of canvases :contentReference[oaicite:11]{index=11}
  - comment threads anchored to canvases or sections :contentReference[oaicite:12]{index=12}
  - embedded files are referenced via messages containing download URLs. :contentReference[oaicite:13]{index=13}

---

# Slack Canvas API Key Info (addendum: getting info from a canvas ID)

---

## How to fetch canvas info via canvas ID

- Use the `files.info` method, passing the **file ID** which corresponds to the canvas. This returns a `file` object that may include `document_content`. :contentReference[oaicite:0]{index=0}
- The response `file` object includes metadata (title, timestamps, etc.) plus potentially a `document_content` field. If `document_content.type == "markdown"`, then you can get the markdown directly. :contentReference[oaicite:1]{index=1}
- If `document_content` is not present (or not markdown), you'll need to rely on export data or public/private download URLs (if available) to retrieve the canvas content. Related permissions and scope apply. :contentReference[oaicite:2]{index=2}

---

## Endpoint & scope notes

- `files.info` is the specific endpoint for fetching info given a file/canvas ID. :contentReference[oaicite:3]{index=3}
- The token/app must have permissions to read the canvas/file (e.g. `files:read` or equivalent) and access to private files if needed. :contentReference[oaicite:4]{index=4}
