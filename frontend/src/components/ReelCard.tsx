import { AnimatePresence, motion, useMotionValue, useTransform } from 'framer-motion'
import type { RecommendedReel } from '../types/recommendation'
import { ReelThumbnail } from './ReelThumbnail'

interface ReelCardProps {
  recommendedReel: RecommendedReel | undefined
  isLoading: boolean
  isMutating: boolean
  onLike: () => void
  onSkip: () => void
}

const SWIPE_THRESHOLD = 120

export function ReelCard({ recommendedReel, isLoading, isMutating, onLike, onSkip }: ReelCardProps) {
  const x = useMotionValue(0)
  const rotate = useTransform(x, [-200, 200], [-12, 12])
  const likeOpacity = useTransform(x, [20, SWIPE_THRESHOLD], [0, 1])
  const skipOpacity = useTransform(x, [-SWIPE_THRESHOLD, -20], [1, 0])

  if (isLoading || !recommendedReel) {
    return (
      <div className="flex h-[600px] w-full max-w-sm items-center justify-center rounded-3xl border border-neutral-800 bg-neutral-900">
        <p className="px-8 text-center text-sm text-neutral-500">
          {isLoading ? 'Loading recommendations…' : "You've caught up — no more reels right now."}
        </p>
      </div>
    )
  }

  const { reel, score } = recommendedReel

  function handleDragEnd(_: unknown, info: { offset: { x: number } }) {
    if (info.offset.x > SWIPE_THRESHOLD) {
      onLike()
    } else if (info.offset.x < -SWIPE_THRESHOLD) {
      onSkip()
    }
    x.set(0)
  }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={reel.id}
        drag={isMutating ? false : 'x'}
        style={{ x, rotate }}
        dragConstraints={{ left: 0, right: 0 }}
        dragElastic={0.7}
        onDragEnd={handleDragEnd}
        initial={{ opacity: 0, scale: 0.96, y: 12 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.96 }}
        transition={{ duration: 0.2 }}
        className="relative flex w-full max-w-sm cursor-grab flex-col overflow-hidden rounded-3xl border border-neutral-800 bg-neutral-900 shadow-xl shadow-black/40 active:cursor-grabbing"
      >
        <motion.span
          style={{ opacity: likeOpacity }}
          className="pointer-events-none absolute left-4 top-4 z-10 rounded-lg border-2 border-emerald-400 px-3 py-1 text-sm font-bold uppercase tracking-wide text-emerald-400"
        >
          Like
        </motion.span>
        <motion.span
          style={{ opacity: skipOpacity }}
          className="pointer-events-none absolute right-4 top-4 z-10 rounded-lg border-2 border-rose-400 px-3 py-1 text-sm font-bold uppercase tracking-wide text-rose-400"
        >
          Skip
        </motion.span>

        <ReelThumbnail emoji={reel.thumbnail_emoji} color={reel.thumbnail_color} className="h-64 w-full" />

        <div className="flex flex-col gap-3 p-5">
          <div className="flex items-center justify-between">
            <span className="rounded-full bg-neutral-800 px-2.5 py-1 text-xs font-medium text-neutral-300">
              {reel.category}
            </span>
            <span className="text-xs text-neutral-500">similarity {score.toFixed(2)}</span>
          </div>
          <h3 className="text-lg font-semibold leading-snug text-neutral-50">{reel.title}</h3>
          <p className="text-sm text-neutral-400">{reel.caption}</p>
          <p className="text-xs text-neutral-500">@{reel.creator}</p>
          <div className="flex flex-wrap gap-1.5">
            {reel.tags.map((tag) => (
              <span
                key={tag}
                className="rounded-full bg-neutral-800/70 px-2 py-0.5 text-[11px] text-neutral-400"
              >
                #{tag}
              </span>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2 border-t border-neutral-800 p-4">
          <button
            onClick={onSkip}
            disabled={isMutating}
            className="flex-1 rounded-xl bg-neutral-800 py-2.5 text-sm font-medium text-neutral-200 transition hover:bg-neutral-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Skip
          </button>
          <button
            onClick={onLike}
            disabled={isMutating}
            className="flex-1 rounded-xl bg-indigo-500 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Like
          </button>
          <button
            disabled
            title="Coming soon"
            className="flex-1 cursor-not-allowed rounded-xl bg-neutral-800/50 py-2.5 text-sm font-medium text-neutral-600"
          >
            Save
          </button>
        </div>
      </motion.div>
    </AnimatePresence>
  )
}
