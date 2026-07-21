import type { InteractionEntry } from '../types/user'

interface RecentInteractionsProps {
  interactions: InteractionEntry[]
}

export function RecentInteractions({ interactions }: RecentInteractionsProps) {
  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-neutral-800 bg-neutral-900 p-4">
      <h2 className="text-xs font-semibold uppercase tracking-wide text-neutral-500">
        Recent interactions
      </h2>
      {interactions.length === 0 ? (
        <p className="text-sm text-neutral-500">
          No interactions yet — like or skip a reel to get started.
        </p>
      ) : (
        <ul className="flex flex-col gap-2">
          {interactions.map((entry, index) => (
            <li
              key={`${entry.reel_id}-${entry.timestamp}-${index}`}
              className="flex items-center gap-2 text-sm"
            >
              <span className={entry.action === 'like' ? 'text-emerald-400' : 'text-neutral-500'}>
                {entry.action === 'like' ? '♥' : '⏭'}
              </span>
              <span className="flex-1 truncate text-neutral-300">{entry.reel_title}</span>
              <span className="shrink-0 text-xs text-neutral-600">{entry.category}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
