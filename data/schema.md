# Data Schema

## Season CSV files (`data/<year>.csv`)

One file per season (e.g. `data/2026.csv`). Each row = one driver.

| Column | Type | Description | Example |
|---|---|---|---|
| `driver` | string | Driver last name | `Russell` |
| `winner` | string | Draft auction owner | `Brandon` |
| `amount_paid` | int | Auction price paid (dollars) | `200` |
| `points` | int | Accumulated F1 championship points this season | `51` |

### Notes
- `amount_paid` of `0` means driver was not contested in the auction (kept for free or undrafted).
- `points` is manually updated after each race weekend.
- Driver names match the filenames in `driver-pics/<Driver>.png`.
- Sorted alphabetically by `driver`.

### Valid `winner` values
`Brandon`, `Devika`
