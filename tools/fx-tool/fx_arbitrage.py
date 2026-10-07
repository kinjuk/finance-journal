"""FX interest arbitrage calculator.

Logic mirrors 'FX Arbitrage Tool.xlsx' (sheet 'FX Arbitrage Calc') cell for cell.
Cell references in comments point to that workbook.

Route A: keep the capital in currency A and earn A's interest.
Route B: convert to currency B, earn B's interest, convert back to A.
Net advantage = Route B result minus Route A result, both in currency A.

Interest is simple, not compounded: rate * days / 365, as in the Excel.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Inputs:
    a_rate: float = 0.02       # B3  A currency interest rate (annual, as a fraction)
    b_rate: float = 0.042      # B4  B currency interest rate (annual, as a fraction)
    spot_out: float = 1.1667   # B5  A/B spot rate out
    fee: float = 0.005         # B6  broker FX conversion fee (as a fraction)
    days: float = 365.0        # B7  holding period in days
    capital: float = 1000.0    # B8  initial capital in A currency
    spot_back: float = 1.171   # B9  A/B spot rate back


@dataclass(frozen=True)
class Outputs:
    net_fx_rate: float         # D3  net FX rate after broker cost
    converted_capital: float   # D4  converted capital (in B currency)
    b_yield: float             # D5  B currency yield for the holding period
    final_b_value: float       # D6  final B currency value
    back_in_a: float           # D7  converted back to A currency
    a_yield: float             # D8  A currency yield for the holding period
    final_a_value: float       # D9  final A currency value (staying in A)
    net_advantage: float       # D10 net advantage (B route vs A route)


def calculate(i: Inputs, fee_on_return: bool = False) -> Outputs:
    """Run the calculation.

    fee_on_return=False reproduces the Excel exactly (fee charged once, on the
    way out). True also deducts the broker fee on the way back, which the
    Excel does not do.
    """
    if i.spot_out <= 0 or i.spot_back <= 0:
        raise ValueError("Spot rates must be greater than zero.")
    if not 0 <= i.fee < 1:
        raise ValueError("Broker fee must be at least 0% and below 100%.")
    if i.days < 0:
        raise ValueError("Holding period cannot be negative.")

    d3 = i.spot_out * (1 - i.fee)             # =B5 * (1 - B6)
    d4 = i.capital * d3                       # =B8 * D3
    d5 = d4 * (i.b_rate * i.days / 365)       # =D4 * (B4 * B7 / 365)
    d6 = d4 + d5                              # =D4 + D5
    d7 = d6 / i.spot_back                     # =D6 / B9
    if fee_on_return:
        d7 *= 1 - i.fee
    d8 = i.capital * (i.a_rate * i.days / 365)  # =B8 * (B3 * B7 / 365)
    d9 = i.capital + d8                       # =B8 + D8
    d10 = d7 - d9                             # =D7 - D9
    return Outputs(d3, d4, d5, d6, d7, d8, d9, d10)
