[![THE WORLD TODAY](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b156-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b156-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

One image summing up 23 November 2026's world news: the AI rout that hit Asian markets, Guterres calling for AI rules before it's too late, and the US lead over China at a record low — plus 28 more stories, a world map with numbered pins, and a DATE CHECK box separating what happened on other days.

## What's inside

- **3 hero stories** — Kospi −3.3% (4,708.54, −161 pts), Guterres at the Bridgetown summit (150 delegates), Asia Power Index 2026 (US 78.9 vs China 73.6, gap 5.3)
- **10 cards** — Bessent/Nvidia, FBI NCIC hack, Trump on Iran strikes, Nasdaq futures +3%, Skubal's $450M Mets deal, Tom Jackson, states vs SpaceX, Anthropic IPO ($107.3B at $83/share), Poland missile claim, Russian nuclear satellite warning
- **18 more stories** in ALSO ON MONDAY, a number strip, a region bar, and a world map with 13 numbered pins
- **DATE CHECK** — stories from other days (Dems 258, Sparta II fire, El Chapo, EU–Indonesia, Nigeria boat, ICJ Myanmar) are listed only there, never as 23 Nov news

## Run

```sh
python3 draw.py        # regenerates entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # validates + writes out/entry.png
```

`main.py` is stdlib-only (no PIL): it parses the PNG header by hand and verifies dimensions, CRCs, size and sha256 before writing.
