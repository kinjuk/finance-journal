import { describe, expect, it } from 'vitest'
import { messageFrom } from './api'

describe('messageFrom', () => {
  it('reads string details', () => expect(messageFrom({ detail: 'No data for: XYZ' }, 'x')).toBe('No data for: XYZ'))
  it('strips pydantic prefix from validation errors', () =>
    expect(messageFrom({ detail: [{ msg: 'Value error, Infeasible: ...' }] }, 'x')).toBe('Infeasible: ...'))
  it('falls back', () => expect(messageFrom(null, 'Request failed (500)')).toBe('Request failed (500)'))
})
