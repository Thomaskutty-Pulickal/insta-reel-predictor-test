import { useMutation, useQueryClient } from '@tanstack/react-query'
import { resetUser } from '../services/api'

export function useResetUser(userId: string | undefined) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: () => resetUser(userId as string),
    onSuccess: (data) => {
      queryClient.setQueryData(['userProfile', userId], data)
      queryClient.invalidateQueries({ queryKey: ['recommendations', userId] })
    },
  })
}
