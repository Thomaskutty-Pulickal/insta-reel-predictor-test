export interface UserSummary {
  id: string
  name: string
  avatar_emoji: string
}

export interface InterestBar {
  category: string
  score: number
}

export interface InteractionEntry {
  reel_id: string
  reel_title: string
  category: string
  action: 'like' | 'skip'
  timestamp: string
}

export interface UserProfile {
  id: string
  name: string
  avatar_emoji: string
  likes: string[]
  dislikes: string[]
  interests: InterestBar[]
  recent_interactions: InteractionEntry[]
}
