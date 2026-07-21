import type { UserProfile } from '../types/user'

interface EmbeddingSummaryProps {
  profile: UserProfile
}

export function EmbeddingSummary({ profile }: EmbeddingSummaryProps) {
  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-neutral-800 bg-neutral-900 p-4">
      <h2 className="text-xs font-semibold uppercase tracking-wide text-neutral-500">
        Embedding summary
      </h2>
      <div>
        <p className="mb-1.5 text-xs text-neutral-500">Seeded likes</p>
        <div className="flex flex-wrap gap-1.5">
          {profile.likes.map((like) => (
            <span
              key={like}
              className="rounded-full bg-emerald-500/10 px-2.5 py-1 text-xs text-emerald-400"
            >
              {like}
            </span>
          ))}
        </div>
      </div>
      <div>
        <p className="mb-1.5 text-xs text-neutral-500">Seeded dislikes</p>
        <div className="flex flex-wrap gap-1.5">
          {profile.dislikes.map((dislike) => (
            <span
              key={dislike}
              className="rounded-full bg-rose-500/10 px-2.5 py-1 text-xs text-rose-400"
            >
              {dislike}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
