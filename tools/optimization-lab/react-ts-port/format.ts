import type { Objective } from './types'

export const OBJECTIVES: { key: Objective; label: string }[] = [
  { key: 'sharpe', label: 'Max Sharpe' },
  { key: 'sortino', label: 'Max Sortino' },
  { key: 'minvol', label: 'Min Volatility' },
]
export const pct = (x: number, d = 2) => `${(x * 100).toFixed(d)}%`
export const num = (x: number, d = 3) => x.toFixed(d)
export const parseTickers = (s: string) => [...new Set(s.split(/[\s,;]+/).map((t) => t.trim().toUpperCase()).filter(Boolean))]
