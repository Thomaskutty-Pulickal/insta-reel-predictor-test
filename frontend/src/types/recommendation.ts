import type { Reel } from './reel'

export interface Explanation {
  similarity_score: number
  reasons: string[]
}

export interface RecommendedReel {
  reel: Reel
  score: number
  explanation: Explanation
}

export interface RecommendationsResponse {
  items: RecommendedReel[]
}
