# Crypto Quant Strategy — 3-Component Ensemble with Vol-Adjusted Intraday Reversal

A defensible, all-weather crypto trading strategy built with a fully out-of-sample
methodology: real execution costs, no look-ahead, and every parameter frozen on the
train set before a single test pass. The emphasis is on **rigor and honesty over a
headline Sharpe** — the notebook documents 20+ rejected experiments alongside what worked.

## Headline result (net of realistic costs)

Universe: 53 USDT spot pairs on Binance (median daily volume > $5M).
Train: 2021-01 → 2023-06 · Test: 2023-07 → 2025-12.
Costs: 15 bps/side for daily signals (10 bps taker + 5 bps slippage), 20 bps/side for the intraday reversal.

| Strategy | SR train | **SR test** | Max DD test | Calmar |
|---|---:|---:|---:|---:|
| BTC Buy & Hold | 0.37 | 1.15 | -32.0% | 1.64 |
| BTC + vol-targeting | 0.39 | 0.86 | -18.5% | 1.01 |
| 2c Ensemble + Overlay | 1.59 | 1.37 | -11.7% | 1.42 |
| **★ 3c Ensemble + Overlay ★** | **1.74** | **1.56** | **-10.7%** | **1.55** |

Headline **SR 1.56** at ~11% volatility (≈52% capital deployed). Since Sharpe is
leverage-invariant, the same edge can be dialed to any risk target (e.g. ~31%/yr at
20% vol with no borrowing) — see §16.4.

## Strategy in one paragraph

Three signals combined by Inverse-Variance weighting, plus a risk overlay:

1. **Volume Momentum Binary** (~52%) — directional volume-momentum binary; the primary alpha source.
2. **Smart TSMOM** (~28%) — vol-managed time-series momentum with a per-asset Sharpe filter; a diversifier.
3. **Vol-Adjusted Intraday Reversal** (~20%) — per-coin >4σ moves at 6h that revert; uncorrelated alpha.
4. **Correlation Regime Overlay** — scales exposure down when cross-sectional correlation spikes.

Grounded in published literature: Moskowitz-Ooi-Pedersen (2012), Moreira-Muir (2017),
Nguyen "AdaptiveTrend" (2026, arXiv:2602.11708), Heston-Korajczyk-Sadka (2010),
Longin-Solnik (2001), Kritzman et al. (2011), López de Prado (HRP).

## How to run

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook strategy.ipynb        # Run All
```

The daily and 6h price data are cached in `data/` (≈8 MB), so the notebook runs
end-to-end without hitting the Binance API. Delete `data/_px_cache.pkl` to force a
fresh download.

## Repository structure

```
.
├── README.md
├── requirements.txt
├── strategy.ipynb          # the full pipeline (sections 1–19)
├── report/
│   ├── REPORT.pdf           # methodology & results whitepaper (with figures)
│   ├── REPORT.md            # markdown source of the report
│   ├── figures/             # charts used in the report
│   └── build_pdf.py         # rebuilds REPORT.pdf from REPORT.md
└── data/
    ├── _px_cache.pkl        # daily OHLCV cache (53 coins, 2021–2025)
    └── _px_6h_cache.pkl     # 6h cache for the intraday reversal
```

A full written walkthrough of the methodology, rationale, and results — with figures — is in
[`report/REPORT.pdf`](report/REPORT.pdf) (markdown source: `report/REPORT.md`).

## Methodology highlights

- **No look-ahead:** every signal uses past-only rolling stats + an explicit `shift(1)`;
  ensemble weights estimated on train only. Verified by per-signal permutation tests (§15).
- **Realistic costs applied end-to-end** (worth ~0.8 of Sharpe vs. gross).
- **Signal Integrity Rubric (§15):** classifies each signal as alpha source vs. diversifier
  via a timing-shuffle test; look-ahead is a hard gate.
- **Robustness (§16):** walk-forward across 6 sub-periods, naive-baseline comparison,
  transaction-cost stress test, capital-efficiency analysis, and a block-bootstrap CI.
- **Honest negative results (§13.1):** funding, stablecoin, idiosyncratic momentum,
  pairs/stat-arb and a continuous Factor Zoo were all tested and rejected.

## Known limitations (disclosed)

- Single train/test split (walk-forward stability checks partially mitigate; a per-fold
  re-fit walk-forward would be the next level of rigor).
- Survivorship bias: the universe requires data through the test period.
- The reversal is the most cost-sensitive and lowest-confidence component (rare 4σ events).
- Bootstrap 95% CI for the Sharpe is wide ([0.02, 2.99]); the edge is real but estimated
  with meaningful uncertainty.

This is a research notebook, not production code.
