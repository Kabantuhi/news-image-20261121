# The World Today — 21 November 2026 in one image

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Kabantuhi/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Kabantuhi/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Entry for the make.fun **news-image-20261121** bounty ($100 prize pool,
top 50 share; entries close Monday 23 November 2026, 08:00 WITA).

One 1024×1024 poster summarising the day's world news:

1. **Russia's biggest air assault** — 400+ drones and 110 missiles strike
   Ukraine overnight; two missiles and a drone land in Poland; PM Tusk calls
   it a deliberate provocation, NATO calls it a grave violation.
2. **COP31 into overtime, no deal** — third draft due Saturday; fossil-fuel
   language stripped; Ethiopia to host COP32.
3. **S&P 500 falls into correction** — AI rout: S&P −3.7% on Friday;
   Nasdaq −5.3%; $4tn wiped from tech in a week.
4. **ICJ ruling echoes on** — Myanmar verdict's fallout spreads; experts say
   it could shape the Israel case.
5. **Gen Z takes to the streets** — youth strikes in 25 countries over living
   costs, climate and conscription.
6. **UK–EU sign post-Brexit deals** — three accords on food, carbon markets
   and youth mobility.
7. **Cancer pill breakthrough** — daraxonrasib trial: tumours undetectable in
   1 in 12 pancreatic cancer patients.

Every headline was verified against reports published on 21 November 2026
(AP, Reuters, BBC, The Times, Carbon Brief, The Telegraph) before the image
was drawn.

## How it works

- `news.json` — the seven verified stories (headline, deck, fact chips).
- `render.py` — draws the poster with PIL + DejaVu fonts only. No network,
  no randomness, no timestamps: running it twice produces byte-identical
  output (sha256 verified).
- `main.py` — entrypoint: validates `entry.png` (PNG, 1024×1024, ≤ 1 MiB)
  and copies it to `/output/entry.png`.
- `entry.png` — the finished poster (1024×1024, ~112 KB).

## Run

```sh
python3 render.py        # regenerate entry.png from news.json
python3 main.py          # write /output/entry.png
```

Python 3.12 with Pillow (`pip install pillow`). No other dependencies.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=c45jj78w&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
