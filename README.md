# bgtutor-assets

Prepared episodes for the Bulgarian Podcast Tutor (bgtutor), the MCP server in
[snonux/totalrecall](https://github.com/snonux/totalrecall) (`cmd/bgtutor`,
docs in `bgtutor/`).

Each folder under `episodes/` is one episode in the format described in
`bgtutor/FORMAT.md` of totalrecall: `meta.json` plus `paragraphs.json`. They
were made by following `bgtutor/PREPARE.md` there.

| Episode | Source | Paragraphs | Level |
|---|---|---|---|
| `002-digital-minimalist-2026` | Deep Questions with Cal Newport, "Can I Be a Digital Minimalist in 2026?" (main segment, ads removed) | 99 | B1 |
| `003-at-protocol-own-data` | Fallthrough, "A Record of One's Own" (transcribed from the audio with Whisper, speakers inferred; Bulgarian notes pitched at A2) | 127 | A2 |

The English text comes from the original podcasts and belongs to their
creators. It is kept here for personal study.

## Adding an episode

Prepare it in a totalrecall checkout (`bgtutor/data/episodes/<id>/`), run
`go run ./cmd/bgtutor validate <id>` and `go run ./cmd/bgtutor publish <id>`,
then copy the folder into `episodes/` here and commit.

## Serving an episode

On f3s, from `f3s/bgtutor` in snonux/conf:

```
just upload-episode episodes/<id>
```
