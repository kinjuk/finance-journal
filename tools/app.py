import streamlit as st

from fx_arbitrage import Inputs, calculate

st.set_page_config(page_title="FX Interest Arbitrage Calculator", layout="centered")
st.title("FX Interest Arbitrage Calculator")

left, right = st.columns(2)

with left:
    st.subheader("INPUTS")
    a_rate = st.number_input("A Currency Interest Rate (%)", value=2.0, step=0.1, format="%.3f")
    b_rate = st.number_input("B Currency Interest Rate (%)", value=4.2, step=0.1, format="%.3f")
    spot_out = st.number_input("A/B Spot Rate Out", value=1.1667, step=0.0001, format="%.4f")
    fee = st.number_input("Broker FX Conversion Fee (%)", value=0.5, step=0.05, format="%.3f")
    days = st.number_input("Holding Period (Days)", value=365.0, step=1.0, format="%.0f")
    capital = st.number_input("Initial Capital (in A currency)", value=1000.0, step=100.0, format="%.2f")
    spot_back = st.number_input("A/B Spot Rate Back", value=1.171, step=0.0001, format="%.4f")
    fee_on_return = st.checkbox(
        "Also charge the broker fee on the return conversion",
        value=False,
        help="Off matches the Excel, which charges the fee only on the way out.",
    )

try:
    out = calculate(
        Inputs(a_rate / 100, b_rate / 100, spot_out, fee / 100, days, capital, spot_back),
        fee_on_return=fee_on_return,
    )
except ValueError as err:
    st.error(str(err))
    st.stop()

with right:
    st.subheader("OUTPUTS")
    rows = {
        "Net FX Rate After Broker Cost": f"{out.net_fx_rate:,.6f}",
        "Converted Capital (in B currency)": f"{out.converted_capital:,.2f}",
        "B Currency Yield (adjusted for time period)": f"{out.b_yield:,.2f}",
        "Final B Currency Value": f"{out.final_b_value:,.2f}",
        "Convert Back to A Currency": f"{out.back_in_a:,.2f}",
        "A Currency Yield (adjusted for time period)": f"{out.a_yield:,.2f}",
        "Final A Currency Value (staying in A)": f"{out.final_a_value:,.2f}",
    }
    st.table(rows)
    st.metric(
        "Net Advantage (B vs A route)",
        f"{out.net_advantage:,.2f}",
        delta=f"{out.net_advantage:+,.2f}",
    )

st.caption(
    "Simple interest: rate x days / 365. Not financial advice. "
    "Rates and fees are entered as percentages."
)
