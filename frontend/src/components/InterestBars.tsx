import { motion } from 'framer-motion'
import type { InterestBar as InterestBarType } from '../types/user'

interface InterestBarsProps {
  interests: InterestBarType[]
  limit?: number
}

/** Bars are scaled relative to the strongest interest in the list (not the
 * raw -1..1 cosine range), so the current #1 interest always reads as a
 * full bar and the gaps between categories stay visually legible. */
export function InterestBars({ interests, limit = 8 }: InterestBarsProps) {
  const visible = interests.slice(0, limit)
  const maxScore = Math.max(...visible.map((interest) => interest.score), 0.01)

  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-neutral-800 bg-neutral-900 p-4">
      <h2 className="text-xs font-semibold uppercase tracking-wide text-neutral-500">Top interests</h2>
      <div className="flex flex-col gap-2.5">
        {visible.map((interest) => {
          const widthPercent = Math.max(0, interest.score / maxScore) * 100
          return (
            <div key={interest.category} className="flex flex-col gap-1">
              <div className="flex items-center justify-between text-xs">
                <span className="font-medium text-neutral-300">{interest.category}</span>
                <span className="tabular-nums text-neutral-500">{interest.score.toFixed(2)}</span>
              </div>
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-neutral-800">
                <motion.div
                  className="h-full rounded-full bg-indigo-500"
                  initial={false}
                  animate={{ width: `${widthPercent}%` }}
                  transition={{ duration: 0.5, ease: 'easeOut' }}
                />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
