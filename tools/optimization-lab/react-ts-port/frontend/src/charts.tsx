import { Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis } from 'recharts'
import { OBJECTIVES, num, pct } from './format'
import type { Objective, OptimizeResponse } from './types'

export const PAL = ['#4f9dff', '#f5b942', '#3ddc97', '#ff6b6b', '#b48cff', '#2ec4d6', '#ff9f68', '#9aa5b1']
const axis = { stroke: 'var(--mut)', fontSize: 12 }

export function Allocation({ data, obj }: { data: OptimizeResponse; obj: Objective }) {
  const cur = data.results[obj]
  const tickers = data.assets.map((a) => a.ticker)
  const donut = cur.ok ? tickers.map((t) => ({ name: t, value: cur.weights[t] })) : []
  const bars = tickers.map((t) => ({ t, ...Object.fromEntries(OBJECTIVES.map((o) => { const r = data.results[o.key]; return [o.key, r.ok ? r.weights[t] : null] })) }))
  return (
    <>
      <div className="grid2">
        <div className="card" aria-label="Allocation donut">
          <ResponsiveContainer width="100%" height={340}>
            <PieChart>
              <Pie data={donut} dataKey="value" innerRadius="58%" outerRadius="85%" paddingAngle={1} stroke="none" label={(e) => `${e.name} ${pct(e.value, 0)}`}>
                {donut.map((_, i) => <Cell key={i} fill={PAL[i % PAL.length]} />)}
              </Pie>
              <Tooltip formatter={(v: number) => pct(v)} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="card" aria-label="Weights by objective">
          <ResponsiveContainer width="100%" height={340}>
            <BarChart data={bars}>
              <CartesianGrid stroke="var(--line)" vertical={false} />
              <XAxis dataKey="t" {...axis} /><YAxis tickFormatter={(v) => pct(v, 0)} {...axis} />
              <Tooltip formatter={(v: number) => pct(v)} /><Legend />
              {OBJECTIVES.map((o, i) => <Bar key={o.key} dataKey={o.key} name={o.label} fill={PAL[i]} radius={[3, 3, 0, 0]} />)}
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="tw">
        <table>
          <thead><tr><th>Objective</th><th>Return</th><th>Vol</th><th>Sharpe</th><th>Sortino</th><th>Turnover vs EW</th><th>At bounds</th></tr></thead>
          <tbody>
            {OBJECTIVES.map((o) => { const r = data.results[o.key]; return r.ok ? (
              <tr key={o.key}><td>{o.label}</td><td>{pct(r.metrics.expected_annual_return)}</td><td>{pct(r.metrics.annual_volatility)}</td>
                <td>{num(r.metrics.sharpe_ratio)}</td><td>{num(r.metrics.sortino_ratio)}</td><td>{pct(r.turnover, 1)}</td>
                <td>{Object.keys(r.at_bounds).join(', ') || '—'}</td></tr>
            ) : <tr key={o.key}><td>{o.label}</td><td colSpan={6}>Solver failed: {r.message}</td></tr> })}
            <tr><td>Equal weight</td><td>{pct(data.equal_weight.expected_annual_return)}</td><td>{pct(data.equal_weight.annual_volatility)}</td>
              <td>{num(data.equal_weight.sharpe_ratio)}</td><td>{num(data.equal_weight.sortino_ratio)}</td><td>0.0%</td><td>—</td></tr>
          </tbody>
        </table>
      </div>
    </>
  )
}

export function Frontier({ data }: { data: OptimizeResponse }) {
  const stars = OBJECTIVES.flatMap((o, i) => { const r = data.results[o.key]; return r.ok ? [{ ...o, i, p: [{ vol: r.metrics.annual_volatility, ret: r.metrics.expected_annual_return }] }] : [] })
  const ew = [{ vol: data.equal_weight.annual_volatility, ret: data.equal_weight.expected_annual_return }]
  return (
    <div className="card" aria-label="Efficient frontier">
      <ResponsiveContainer width="100%" height={520}>
        <ScatterChart margin={{ top: 10, right: 20, bottom: 24, left: 4 }}>
          <CartesianGrid stroke="var(--line)" />
          <XAxis type="number" dataKey="vol" name="Volatility" domain={['auto', 'auto']} tickFormatter={(v) => pct(v, 0)} label={{ value: 'Volatility', position: 'bottom', fill: 'var(--mut)' }} {...axis} />
          <YAxis type="number" dataKey="ret" name="Return" domain={['auto', 'auto']} tickFormatter={(v) => pct(v, 0)} {...axis} />
          <Tooltip formatter={(v: number) => pct(v)} cursor={{ strokeDasharray: '3 3' }} /><Legend verticalAlign="bottom" wrapperStyle={{ paddingTop: 16 }} />
          <Scatter name="Random feasible portfolios" data={data.cloud} fill="var(--mut)" fillOpacity={0.35} shape="circle" legendType="circle" />
          <Scatter name="Efficient frontier" data={data.frontier} line={{ stroke: PAL[0], strokeWidth: 3 }} lineType="joint" shape={() => <g />} fill={PAL[0]} legendType="line" />
          {stars.map((s) => <Scatter key={s.key} name={s.label} data={s.p} fill={PAL[s.i + 1]} shape="star" legendType="star" />)}
          <Scatter name="Equal weight" data={ew} fill={PAL[3]} shape="diamond" legendType="diamond" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  )
}
