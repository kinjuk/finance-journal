import { useCallback, useEffect, useRef, useState } from 'react'
import { ApiError, optimize } from './api'
import { Allocation, Frontier } from './charts'
import { OBJECTIVES, num, parseTickers, pct } from './format'
import Tabs from './Tabs'
import type { Objective, OptimizeRequest, OptimizeResponse } from './types'

const TABS = ['Allocation', 'Frontier']
type State = { status: 'loading' | 'ready' | 'error'; data?: OptimizeResponse; error?: string; slow?: boolean }

export default function App() {
  const [dark, setDark] = useState(() => matchMedia('(prefers-color-scheme: dark)').matches)
  const [tickers, setTickers] = useState('SPY, BND, GLD, QQQ, VTI')
  const [live, setLive] = useState(false)
  const [start, setStart] = useState('2015-01-01')
  const [end, setEnd] = useState('2025-10-23')
  const [minW, setMinW] = useState(5)
  const [maxW, setMaxW] = useState(40)
  const [rf, setRf] = useState(4)
  const [est, setEst] = useState<'arith' | 'log'>('arith')
  const [obj, setObj] = useState<Objective>('sharpe')
  const [tab, setTab] = useState(TABS[0])
  const [state, setState] = useState<State>({ status: 'loading' })
  const first = useRef(true)
  const ctl = useRef<AbortController | null>(null)

  useEffect(() => { document.documentElement.dataset.theme = dark ? 'dark' : 'light' }, [dark])

  const run = useCallback(async () => {
    ctl.current?.abort()
    const c = (ctl.current = new AbortController())
    const req: OptimizeRequest = { tickers: parseTickers(tickers), start, end: live ? null : end, min_weight: minW / 100, max_weight: maxW / 100, rf: rf / 100, estimator: est }
    setState((s) => ({ ...s, status: 'loading', slow: false }))
    const slow = setTimeout(() => setState((s) => (s.status === 'loading' ? { ...s, slow: true } : s)), 4000)
    try {
      const data = await optimize(req, c.signal)
      setState({ status: 'ready', data })
    } catch (e) {
      if (c.signal.aborted) return
      setState((s) => ({ ...s, status: 'error', error: e instanceof ApiError ? e.message : 'Cannot reach the API. Is the backend running?' }))
    } finally { clearTimeout(slow) }
  }, [tickers, start, end, live, minW, maxW, rf, est])

  useEffect(() => { void run() }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const { data, status } = state
  const cur = data?.results[obj]
  const k = cur?.ok && data ? [
    ['Expected return', pct(cur.metrics.expected_annual_return), (cur.metrics.expected_annual_return - data.equal_weight.expected_annual_return) * 100, 1, 'pp'],
    ['Volatility', pct(cur.metrics.annual_volatility), (cur.metrics.annual_volatility - data.equal_weight.annual_volatility) * 100, -1, 'pp'],
    ['Sharpe', num(cur.metrics.sharpe_ratio), cur.metrics.sharpe_ratio - data.equal_weight.sharpe_ratio, 1, ''],
    ['Sortino', num(cur.metrics.sortino_ratio), cur.metrics.sortino_ratio - data.equal_weight.sortino_ratio, 1, ''],
  ] as const : []
  const pinned = cur?.ok ? Object.entries(cur.at_bounds).map(([t, s]) => `${t} @ ${s} (${pct(cur.weights[t], 0)})`) : []

  const animateIn = first.current
  if (status === 'ready') first.current = false

  return (
    <div className="app">
      <aside>
        <h3>Optimization Lab</h3>
        <button className="btn" onClick={() => setDark(!dark)}>{dark ? 'Light mode' : 'Dark mode'}</button>
        <div className="f"><label htmlFor="tk">Tickers (any Yahoo symbol)</label><input id="tk" type="text" value={tickers} onChange={(e) => setTickers(e.target.value)} /></div>
        <div className="f"><label htmlFor="st">Start</label><input id="st" type="date" value={start} onChange={(e) => setStart(e.target.value)} /></div>
        <div className="f"><label htmlFor="en">End</label><input id="en" type="date" value={end} disabled={live} onChange={(e) => setEnd(e.target.value)} />
          <label className="chk"><input type="checkbox" checked={live} onChange={(e) => setLive(e.target.checked)} /> Live (end = today)</label></div>
        <div className="f"><label htmlFor="mn">Min weight: {minW}%</label><input id="mn" type="range" min={0} max={30} value={minW} onChange={(e) => setMinW(+e.target.value)} /></div>
        <div className="f"><label htmlFor="mx">Max weight: {maxW}%</label><input id="mx" type="range" min={10} max={100} value={maxW} onChange={(e) => setMaxW(+e.target.value)} /></div>
        <div className="f"><label htmlFor="rf">Risk-free rate: {rf.toFixed(2)}%</label><input id="rf" type="range" min={0} max={8} step={0.25} value={rf} onChange={(e) => setRf(+e.target.value)} /></div>
        <div className="f"><label>Return estimator</label><div className="seg">
          <button className={est === 'arith' ? 'on' : ''} onClick={() => setEst('arith')}>Arithmetic (consistent)</button>
          <button className={est === 'log' ? 'on' : ''} onClick={() => setEst('log')}>Legacy log-mean</button></div></div>
        <button className="btn primary" disabled={status === 'loading'} onClick={() => void run()}>{status === 'loading' ? 'Optimizing…' : 'Run optimization'}</button>
      </aside>
      <main aria-busy={status === 'loading'}>
        <h1>Optimization Lab</h1>
        {data && <div className="cap">{data.period.start} → {data.period.end} · {data.period.days.toLocaleString()} days · estimator: {data.assumptions.estimator} · in-sample historical estimates, not forecasts</div>}
        {status === 'loading' && state.slow && <div className="note">Waking the server (free hosting sleeps when idle). This can take up to a minute.</div>}
        {status === 'error' && <div className="warn" role="alert">{state.error}</div>}
        {data && (
          <div className={status === 'loading' ? 'dim' : ''}>
            <div className="seg row">{OBJECTIVES.map((o) => <button key={o.key} className={o.key === obj ? 'on' : ''} onClick={() => setObj(o.key)}>{o.label}</button>)}</div>
            {cur && !cur.ok && <div className="warn" role="alert">Solver failed for this objective: {cur.message}</div>}
            <div className="kpis">{k.map(([l, v, d, g, u], i) => (
              <div key={l} className={`kpi${animateIn ? ' in' : ''}`} style={{ ['--i' as string]: i }}>
                <div className="l">{l}</div><div className="v">{v}</div>
                <div className={`d ${d * g >= 0 ? 'up' : 'dn'}`}>{d >= 0 ? '+' : ''}{d.toFixed(u ? 2 : 3)}{u && ' pp'} vs equal-wt</div></div>))}</div>
            {pinned.length > 0 && <div className="warn"><b>Constraints are driving this result.</b> Pinned at bounds: {pinned.join(', ')}. The optimizer wants more than you allow.</div>}
            <Tabs tabs={TABS} value={tab} onChange={setTab} />
            <div className="pane" key={tab}>{tab === 'Allocation' ? <Allocation data={data} obj={obj} /> : <Frontier data={data} />}</div>
          </div>
        )}
      </main>
    </div>
  )
}
