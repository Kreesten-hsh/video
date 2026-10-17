# Unit economics: AGENT404 (Programmatic Video Engine & Studio)

Every number below comes from the input file. Nothing is looked up or guessed.

## One video

| line | per video |
| --- | ---: |
| Price | $62.50 |
| Voiceover TTS / ElevenLabs API | -$0.40 |
| Whisper alignment & compute | -$0.15 |
| Cloud storage & delivery | -$0.25 |
| Payment fees (Stripe 2.9% + 0.30€) | -$2.11 |
| **Contribution** (what each video leaves to pay the fixed costs) | **$59.59** (95%) |

## The margin that matters

Fixed costs: $55 a month (Dev server & infrastructure $30, Outbound OSINT tools & hosting $25).

- **Break-even: 1 videos a day.** Below that you lose money every month.
- **Profit margin at your plan** (3 a day): **94%** of every sale, after every cost.
- Capacity: 20 a day.

## Year 1, month by month

| month | videos a day | revenue | profit | cumulative (after $200 startup) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | $1,875 | $1,733 | $1,533 |
| 2 | 2 | $3,750 | $3,520 | $5,053 |
| 3 | 2 | $3,750 | $3,520 | $8,574 |
| 4 | 3 | $5,625 | $5,308 | $13,882 |
| 5 | 3 | $5,625 | $5,308 | $19,190 |
| 6 | 4 | $7,500 | $7,096 | $26,286 |
| 7 | 4 | $7,500 | $7,096 | $33,381 |
| 8 | 5 | $9,375 | $8,884 | $42,265 |
| 9 | 5 | $9,375 | $8,884 | $51,148 |
| 10 | 5 | $9,375 | $8,884 | $60,032 |
| 11 | 6 | $11,250 | $10,671 | $70,703 |
| 12 | 6 | $11,250 | $10,671 | $81,374 |

- **Year 1 operating profit: $81,574** on $86,250 of revenue.
- After the $200 startup spend: $81,374.
- Startup money earned back: month 1.
- Cash you need before it pays for itself: **$200**.

## What if

| scenario | margin at plan | break-even a day | year 1 profit |
| --- | ---: | ---: | ---: |
| Base plan | 94% | 1 | $81,574 |
| Price -10% | 94% | 1 | $72,949 |
| Volume -20% | 94% | 1 | $65,127 |
| Unit costs +15% | 94% | 1 | $80,972 |

No red flags in these numbers. They are only as good as the inputs: check every cost against a real quote.
