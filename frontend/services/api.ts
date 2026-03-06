import { Agent, AgentLeaderboardEntry, AgentRun, APIKey, CreatorStats, InstalledAgent, MarketplaceAgent, NotificationItem, PlatformAnalytics, RuntimeLog, RuntimeRunResponse, StakingPosition, StoreAgent, StoreReview, Transaction, WalletBalance } from '@/types';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost';

function getAuthHeaders(): Record<string, string> {
  if (typeof window === 'undefined') return {};
  const token = window.localStorage.getItem('agentcoin_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
      ...(options?.headers || {}),
    },
  });

  if (!res.ok) {
    throw new Error(`API error ${res.status}`);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) => request<T>(path, { method: 'POST', body: JSON.stringify(body ?? {}) }),
  delete: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
};

export const API = {
  register: async (payload: { email: string; username: string; password: string }) => api.post('/api/v1/auth/register', payload),
  login: async (payload: { email: string; password: string }) => api.post<{ access_token: string; token_type: string }>('/api/v1/auth/login', payload),
  me: async () => api.get('/api/v1/auth/me'),

  getApiKeys: async () => api.get<APIKey[]>('/api/v1/api-keys'),
  createApiKey: async (name: string) => api.post<APIKey>('/api/v1/api-keys/create', { name }),
  deleteApiKey: async (id: number) => api.delete(`/api/v1/api-keys/${id}`),

  getNotifications: async () => api.get<NotificationItem[]>('/api/v1/notifications'),
  readNotification: async (id: number) => api.post<NotificationItem>(`/api/v1/notifications/read/${id}`),
  getPlatformAnalytics: async () => api.get<PlatformAnalytics>('/api/v1/analytics/platform'),

  getAgents: async () => api.get<Agent[]>('/api/v1/agents'),
  getAgent: async (id: string) => api.get<Agent>(`/api/v1/agents/${id}`),

  publishAgent: async (id: string, payload: { title?: string; description?: string; category: string; tags: string[]; price_per_run: number; price_per_month: number }) => api.post(`/api/v1/agents/${id}/publish`, payload),
  unpublishAgent: async (id: string) => api.post(`/api/v1/agents/${id}/unpublish`, {}),
  getStoreAgents: async (params?: { category?: string; price?: number; rating?: number; popularity?: string }) => {
    const q = new URLSearchParams();
    if (params?.category) q.set('category', params.category);
    if (params?.price) q.set('price', String(params.price));
    if (params?.rating) q.set('rating', String(params.rating));
    if (params?.popularity) q.set('popularity', params.popularity);
    const query = q.toString();
    return api.get<StoreAgent[]>(`/api/v1/store/agents${query ? `?${query}` : ''}`);
  },
  getStoreAgent: async (id: string | number) => api.get<StoreAgent>(`/api/v1/store/agents/${id}`),
  installStoreAgent: async (agent_id: string) => api.post<InstalledAgent>(`/api/v1/store/install/${agent_id}`),
  getMyInstalledAgents: async () => api.get<InstalledAgent[]>('/api/v1/store/my-agents'),
  reviewStoreAgent: async (payload: { agent_id: string; rating: number; review?: string }) => api.post<StoreReview>('/api/v1/store/review', payload),
  getStoreReviews: async (agent_id: string) => api.get<StoreReview[]>(`/api/v1/store/reviews/${agent_id}`),
  getAgentLeaderboard: async () => api.get<AgentLeaderboardEntry[]>('/api/v1/agents/leaderboard'),
  getCreatorStats: async () => api.get<CreatorStats>('/api/v1/agents/creator/stats'),
  createAgent: async (payload: Record<string, unknown>) => api.post('/api/v1/agents/create', payload),
  runAgent: async (id: string, input: string) => api.post<AgentRun>(`/api/v1/agents/${id}/run`, { input }),

  runAgentRuntime: async (agent_id: string, input: string) => api.post<RuntimeRunResponse>('/api/v1/runtime/run-agent', { agent_id, input }),
  getRuntimeLogs: async (agent_id: string) => api.get<RuntimeLog[]>(`/api/v1/runtime/logs/${agent_id}`),
  deleteAgent: async (id: string) => api.delete(`/api/v1/agents/${id}`),
  getMarketplaceAgents: async () => api.get<MarketplaceAgent[]>('/api/v1/marketplace/agents'),
  buyMarketplaceAgent: async (agent_id: string) => api.post('/api/v1/marketplace/buy', { agent_id }),
  getWalletBalance: async () => api.get<WalletBalance>('/api/v1/wallet/balance'),
  transferWallet: async (to: string, amount: number) => api.post('/api/v1/wallet/transfer', { to, amount }),
  getTransactions: async () => api.get<Transaction[]>('/api/v1/wallet/transactions'),
  getStaking: async () => api.get<StakingPosition>('/api/v1/staking'),
  stake: async (amount: number) => api.post('/api/v1/staking', { action: 'stake', amount }),
  unstake: async (amount: number) => api.post('/api/v1/staking', { action: 'unstake', amount }),
};
