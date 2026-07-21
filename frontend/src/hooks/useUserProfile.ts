import { useQuery } from '@tanstack/react-query'
import { fetchUserProfile } from '../services/api'

export function useUserProfile(userId: string | undefined) {
  return useQuery({
    queryKey: ['userProfile', userId],
    queryFn: () => fetchUserProfile(userId as string),
    enabled: Boolean(userId),
  })
}
