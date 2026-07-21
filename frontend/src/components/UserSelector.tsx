import type { UserSummary } from '../types/user'

interface UserSelectorProps {
  users: UserSummary[]
  selectedUserId: string | undefined
  onSelect: (userId: string) => void
}

export function UserSelector({ users, selectedUserId, onSelect }: UserSelectorProps) {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-xs font-semibold uppercase tracking-wide text-neutral-500">Viewing as</h2>
      <div className="flex flex-col gap-2">
        {users.map((user) => {
          const isSelected = user.id === selectedUserId
          return (
            <button
              key={user.id}
              onClick={() => onSelect(user.id)}
              className={`flex items-center gap-3 rounded-xl border px-3 py-2.5 text-left transition ${
                isSelected
                  ? 'border-indigo-500 bg-indigo-500/10'
                  : 'border-neutral-800 bg-neutral-900 hover:border-neutral-700'
              }`}
            >
              <span className="text-2xl">{user.avatar_emoji}</span>
              <span className="font-medium text-neutral-100">{user.name}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
