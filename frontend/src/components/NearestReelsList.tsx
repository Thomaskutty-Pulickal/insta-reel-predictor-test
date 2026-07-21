import type { RecommendedReel } from '../types/recommendation'

interface NearestReelsListProps {
  items: RecommendedReel[]
  isLoading: boolean
}

/** Unlike the swipeable feed, this list ignores interaction history - it's
 * a diagnostic read of "what is the user's embedding closest to right now",
 * so already-liked/skipped reels can still show up here. */
export function NearestReelsList({ items, isLoading }: NearestReelsListProps) {
  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-neutral-800 bg-neutral-900 p-4">
      <h2 className="text-xs font-semibold uppercase tracking-wide text-neutral-500">
        Top {items.length || 10} nearest reels
      </h2>
      {isLoading ? (
        <p className="text-sm text-neutral-500">Computing neighborhood…</p>
      ) : (
        <ol className="flex flex-col gap-2">
          {items.map((item, index) => (
            <li key={item.reel.id} className="flex items-center gap-2 text-sm">
              <span className="w-4 text-xs text-neutral-600">{index + 1}</span>
              <span>{item.reel.thumbnail_emoji}</span>
              <span className="flex-1 truncate text-neutral-300">{item.reel.title}</span>
              <span className="shrink-0 tabular-nums text-xs text-neutral-500">
                {item.score.toFixed(2)}
              </span>
            </li>
          ))}
        </ol>
      )}
    </div>
  )
}
