import { Agent, AgentLeaderboardEntry, AgentRun, CreatorStats, MarketplaceAgent, RuntimeLog, RuntimeRunResponse, StakingPosition, Transaction, WalletBalance } from '@/types';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
  });

  if (!res.ok) {
    throw new Error(`API error ${res.status}`);
  }

  return res.json();
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) => request<T>(path, { method: 'POST', body: JSON.stringify(body ?? {}) }),
  delete: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
};

export const API = {
  getAgents: async () => api.get<Agent[]>('/api/v1/agents'),
  getAgent: async (id: string) => api.get<Agent>(`/api/v1/agents/${id}`),
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
