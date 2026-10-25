import type { OptimizeRequest, OptimizeResponse } from './types'

const BASE = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

export function messageFrom(body: unknown, fallback: string): string {
  const d = (body as { detail?: unknown } | null)?.detail
  if (typeof d === 'string') return d
  if (Array.isArray(d) && d.length) return String((d[0] as { msg?: string }).msg ?? fallback).replace(/^Value error, /, '')
  return fallback
}

export async function optimize(req: OptimizeRequest, signal?: AbortSignal): Promise<OptimizeResponse> {
  const res = await fetch(`${BASE}/api/optimize`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(req), signal,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => null)
    throw new ApiError(res.status, messageFrom(body, `Request failed (${res.status})`))
  }
  return res.json() as Promise<OptimizeResponse>
}
