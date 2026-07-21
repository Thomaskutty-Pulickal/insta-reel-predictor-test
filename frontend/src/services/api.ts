import type { RecommendationsResponse } from '../types/recommendation'
import type { UserProfile, UserSummary } from '../types/user'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8010/api'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!response.ok) {
    const body = await response.text()
    throw new Error(`${response.status} ${response.statusText}: ${body}`)
  }
  return response.json() as Promise<T>
}

export function fetchUsers(): Promise<UserSummary[]> {
  return request('/users')
}

export function fetchUserProfile(userId: string): Promise<UserProfile> {
  return request(`/users/${userId}`)
}

export function fetchRecommendations(userId: string, count = 6): Promise<RecommendationsResponse> {
  return request(`/users/${userId}/recommendations?count=${count}`)
}

export function fetchNearestReels(userId: string, count = 10): Promise<RecommendationsResponse> {
  return request(`/users/${userId}/nearest-reels?count=${count}`)
}

export function postInteraction(
  userId: string,
  reelId: string,
  action: 'like' | 'skip',
): Promise<{ user: UserProfile }> {
  return request(`/users/${userId}/interactions`, {
    method: 'POST',
    body: JSON.stringify({ reel_id: reelId, action }),
  })
}

export function resetUser(userId: string): Promise<UserProfile> {
  return request(`/users/${userId}/reset`, { method: 'POST' })
}
