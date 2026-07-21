import { useQuery } from '@tanstack/react-query'
import { fetchNearestReels } from '../services/api'

export function useNearestReels(userId: string | undefined) {
  return useQuery({
    queryKey: ['nearestReels', userId],
    queryFn: () => fetchNearestReels(userId as string, 10),
    enabled: Boolean(userId),
  })
}
