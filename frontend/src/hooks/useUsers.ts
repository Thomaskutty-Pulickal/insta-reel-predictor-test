import { useQuery } from '@tanstack/react-query'
import { fetchUsers } from '../services/api'

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  })
}
