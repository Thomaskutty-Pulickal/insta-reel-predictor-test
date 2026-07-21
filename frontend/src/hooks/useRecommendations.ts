import { useQuery } from '@tanstack/react-query'
import { fetchRecommendations } from '../services/api'

const BATCH_SIZE = 6

export function useRecommendations(userId: string | undefined) {
  return useQuery({
    queryKey: ['recommendations', userId],
    queryFn: () => fetchRecommendations(userId as string, BATCH_SIZE),
    enabled: Boolean(userId),
  })
}
