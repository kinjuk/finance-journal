import { describe, expect, it } from 'vitest'
import { num, parseTickers, pct } from './format'

describe('format', () => {
  it('formats percentages and numbers', () => {
    expect(pct(0.14286)).toBe('14.29%')
    expect(num(0.783683)).toBe('0.784')
  })
  it('parses, uppercases and dedupes tickers', () => {
    expect(parseTickers('spy, bnd;  GLD spy')).toEqual(['SPY', 'BND', 'GLD'])
    expect(parseTickers(' , ')).toEqual([])
  })
})
