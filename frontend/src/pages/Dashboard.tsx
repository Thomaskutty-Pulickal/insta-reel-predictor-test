import { useState } from 'react'
import { EmbeddingSummary } from '../components/EmbeddingSummary'
import { ExplanationPanel } from '../components/ExplanationPanel'
import { ReelCard } from '../components/ReelCard'
import { UserSelector } from '../components/UserSelector'
import { useReelFeed } from '../hooks/useReelFeed'
import { useUserProfile } from '../hooks/useUserProfile'
import { useUsers } from '../hooks/useUsers'

export function Dashboard() {
  const { data: users } = useUsers()
  const [selectedUserId, setSelectedUserId] = useState<string | undefined>(undefined)

  // Default to the first user once the list loads, without overriding an
  // explicit choice the viewer already made.
  const activeUserId = selectedUserId ?? users?.[0]?.id

  const { data: profile } = useUserProfile(activeUserId)
  const feed = useReelFeed(activeUserId)

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100">
      <header className="border-b border-neutral-900 px-6 py-4">
        <h1 className="text-lg font-semibold">Reel Recommender Lab</h1>
        <p className="text-sm text-neutral-500">
          An embedding-based recommendation engine, visualized live.
        </p>
      </header>

      <main className="mx-auto flex max-w-6xl flex-col gap-6 px-6 py-8 lg:flex-row lg:items-start">
        <aside className="flex w-full flex-col gap-6 lg:w-72 lg:shrink-0">
          {users && (
            <UserSelector users={users} selectedUserId={activeUserId} onSelect={setSelectedUserId} />
          )}
          {profile && <EmbeddingSummary profile={profile} />}
        </aside>

        <section className="flex flex-1 justify-center">
          <ReelCard
            recommendedReel={feed.current}
            isLoading={feed.isLoading}
            isMutating={feed.isMutating}
            onLike={feed.like}
            onSkip={feed.skip}
          />
        </section>

        <aside className="flex w-full flex-col gap-6 lg:w-80 lg:shrink-0">
          <ExplanationPanel explanation={feed.current?.explanation} />
        </aside>
      </main>
    </div>
  )
}
