import { useMutation, useQueryClient } from '@tanstack/react-query'
import { postInteraction } from '../services/api'

export function useInteraction(userId: string | undefined) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ reelId, action }: { reelId: string; action: 'like' | 'skip' }) =>
      postInteraction(userId as string, reelId, action),
    onSuccess: (data) => {
      // The interaction response already carries the fully refreshed
      // profile (new interests, new history) - write it straight into the
      // cache instead of triggering a second round trip.
      queryClient.setQueryData(['userProfile', userId], data.user)
      // The user's embedding just moved, so the nearest-neighbors
      // visualization is stale - it has no equivalent free ride, so refetch.
      queryClient.invalidateQueries({ queryKey: ['nearestReels', userId] })
    },
  })
}
