import { useLayoutEffect, useRef, useState } from 'react'

interface Props { tabs: string[]; value: string; onChange: (t: string) => void }

/** Single sliding indicator (transform only); no animation on first paint. */
export default function Tabs({ tabs, value, onChange }: Props) {
  const refs = useRef<Record<string, HTMLButtonElement | null>>({})
  const measured = useRef(false)
  const [ind, setInd] = useState({ x: 0, w: 0, animate: false })
  useLayoutEffect(() => {
    const b = refs.current[value]
    if (b) setInd({ x: b.offsetLeft, w: b.offsetWidth, animate: measured.current })
    measured.current = true
  }, [value, tabs])
  return (
    <div className="tabs" role="tablist">
      {tabs.map((t) => (
        <button key={t} ref={(el) => { refs.current[t] = el }} role="tab" aria-selected={t === value}
          className={t === value ? 'on' : ''} onClick={() => onChange(t)}>{t}</button>
      ))}
      <span className="ind" style={{ transform: `translateX(${ind.x}px) scaleX(${ind.w / 100})`, transition: ind.animate ? undefined : 'none' }} />
    </div>
  )
}
