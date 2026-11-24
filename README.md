# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/curryfrizz/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/curryfrizz/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

**The World Today** — one image summing up the world news of **Monday
23 November 2026**, drawn as a one-page newspaper front page with the date
in a banner under the masthead. A Python 3.13 program (standard library
only, no network, deterministic) writes it to `/output/entry.png`
(1024×1024 PNG, ~149 KB). This is the third, densest edition of the
page: no illustration, an all-text lead, a THE DAY IN NUMBERS strip,
nine story cards and an IN BRIEF block — some 41 fact lines covering
the day's stories on one page.

The day's stories on the page:

1. **Europe — War:** a Russian drone collapses a five-storey block in
   Dymer near Kyiv (3 dead, 14 missing); the Russian cargo ship Sparta II
   still burns off Finland after a drone strike; Polish prosecutors say
   three Russian Kh-101 missiles crossed into Poland and NATO's council
   meets on Monday.
2. **Climate — COP31:** the longest climate summit on record collapses
   in Antalya with no deal after the final draft omits any mention of
   fossil fuels; the EU and UK reject it.
3. **Middle East:** Bahrain demands UN action after an Iranian strike on
   a Sitra Island site wounds two; two tankers are hit in the Strait of
   Hormuz; Saudi forces intercept a Houthi missile.
4. **Asia — Disaster:** Indonesian police remove 24 body bags from the
   burned-out Cikande candy factory in Serang, Banten; 29 workers still
   missing, search resumes Monday.
5. **Sport:** India declare on a record 720/9 against New Zealand in the
   Wellington Test; Liverpool rout 10-man Manchester United.
6. **Africa — Sudan:** drone strikes hit homes and a UN building in
   Khartoum; 24 civilians are killed in South Sudan.

Plus a ten-line IN BRIEF block (North Korea's Kim on security, WHO's
Ebola plea, Nigeria revenge attacks, South Korea's education minister
resigning over AI cheating, Nepal–India talks, Israel coalition talks
failing, Bolsonaro stable in intensive care, Lebanon explosives
arrests, Lisbon cost-of-living march, Soweto derby final) and an ALSO
TODAY ticker (UN lethal-AI weapons talks, UK–Ukraine drone deal).

The image is drawn by `draw_image_v3.py` (Pillow, deterministic) and
committed as `entry.png`; `main.py` copies it to the output directory.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=wnr0v57x&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
