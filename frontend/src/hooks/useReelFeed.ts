import { useEffect, useState } from 'react'
import { useInteraction } from './useInteraction'
import { useRecommendations } from './useRecommendations'

/** Drives the swipeable reel feed: holds the current batch's position,
 * applies a like/skip, and pulls a fresh batch once the current one is
 * exhausted (the backend naturally excludes everything already liked or
 * skipped, so a refetch never repeats a reel). */
export function useReelFeed(userId: string | undefined) {
  const { data, isLoading, isFetching, refetch } = useRecommendations(userId)
  const interaction = useInteraction(userId)
  const [index, setIndex] = useState(0)

  // Switching users (or a reset) means a brand-new batch - start over.
  useEffect(() => {
    setIndex(0)
  }, [userId])

  const items = data?.items ?? []
  const current = items[index]

  async function respond(action: 'like' | 'skip') {
    if (!current) return
    await interaction.mutateAsync({ reelId: current.reel.id, action })

    const nextIndex = index + 1
    if (nextIndex >= items.length) {
      await refetch()
      setIndex(0)
    } else {
      setIndex(nextIndex)
    }
  }

  return {
    current,
    isLoading: isLoading || (isFetching && items.length === 0),
    isMutating: interaction.isPending,
    like: () => respond('like'),
    skip: () => respond('skip'),
  }
}
