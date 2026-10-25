export type Objective = 'sharpe' | 'sortino' | 'minvol'

export interface OptimizeRequest {
  tickers: string[]
  start: string
  end: string | null
  min_weight: number
  max_weight: number
  rf: number
  estimator: 'arith' | 'log'
}
export interface Metrics {
  expected_annual_return: number
  annual_volatility: number
  sharpe_ratio: number
  sortino_ratio: number
}
export type Result =
  | { ok: true; weights: Record<string, number>; metrics: Metrics; at_bounds: Record<string, 'min' | 'max'>; turnover: number; message: string }
  | { ok: false; message: string }
export interface Point { vol: number; ret: number }
export interface OptimizeResponse {
  period: { start: string; end: string; days: number }
  assumptions: { estimator: string; risk_free: number; min_weight: number; max_weight: number }
  results: Record<Objective, Result>
  equal_weight: Metrics
  frontier: Point[]
  cloud: Point[]
  assets: { ticker: string; ret: number; vol: number }[]
  correlation: { labels: string[]; matrix: number[][] }
}
