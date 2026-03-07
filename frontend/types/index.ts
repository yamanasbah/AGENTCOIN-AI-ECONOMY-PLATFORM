export type Agent = {
  id: string;
  name: string;
  type: string;
  status: string;
  runs: number;
  system_prompt?: string;
  tools?: string[];
  execution_cost?: number;
};

export type AgentRun = {
  id: string;
  input: string;
  output: string;
  created_at: string;
};

export type MarketplaceAgent = {
  id: string;
  name: string;
  description: string;
  price_per_run: number;
  rating: number;
  usage_count: number;
};

export type StoreAgent = {
  id: number;
  agent_id: string;
  title: string;
  description?: string;
  category?: string;
  price_per_run: number;
  price_per_month: number;
  rating: number;
  usage_count: number;
  created_at: string;
  creator_user_id: number;
  creator_username: string;
  total_runs: number;
};

export type InstalledAgent = {
  id: number;
  user_id: number;
  agent_id: string;
  installed_at: string;
  active: boolean;
};

export type StoreReview = {
  id: number;
  agent_id: string;
  user_id: number;
  rating: number;
  review?: string;
  created_at: string;
};

export type WalletBalance = {
  balance: number;
  locked?: number;
};

export type Transaction = {
  id: string;
  amount: number;
  to: string;
  type: string;
  created_at: string;
};

export type StakingPosition = {
  locked_tokens: number;
  unlock_time: string;
};


export type RuntimeLog = {
  id: string;
  agent_id: string;
  input_text?: string;
  output_text?: string;
  status: string;
  execution_cost: number;
  tokens_used: number;
  created_at: string;
};

export type RuntimeRunResponse = {
  task_id: string;
  status: string;
};


export type AgentLeaderboardEntry = {
  id: string;
  name: string;
  owner_user_id: number;
  total_earnings: number;
  total_runs: number;
};

export type CreatorStats = {
  total_agents: number;
  total_earnings: number;
  total_runs: number;
};


export type APIKey = {
  id: number;
  name: string;
  key: string;
  created_at: string;
  is_active: boolean;
};

export type NotificationItem = {
  id: number;
  title: string;
  message: string;
  read: boolean;
  created_at: string;
};

export type PlatformAnalytics = {
  total_users: number;
  total_agents: number;
  total_runs: number;
  total_transactions: number;
  platform_revenue: number;
};

export type AdminAnalytics = {
  total_users: number;
  total_agents: number;
  total_runs: number;
  total_transactions: number;
  total_tokens_staked: number;
  total_marketplace_volume: number;
  platform_revenue: number;
};

export type AdminTreasury = {
  id: number;
  wallet_id: string;
  total_revenue: number;
  total_distributed: number;
  created_at: string;
};

export type RevenueSummary = {
  platform_revenue: number;
  total_distributed: number;
  net_revenue: number;
};

export type ModerationAgent = {
  id: string;
  name: string;
  owner_user_id: number;
  agent_type: string;
  agent_status: 'pending' | 'approved' | 'rejected' | 'banned';
  created_at: string;
};

export type AgentFlag = {
  id: number;
  agent_id: string;
  reason: string;
  flag_count: number;
  created_at: string;
};

export type SystemHealth = {
  api_latency_ms: number;
  queue_size: number;
  agent_execution_rate: number;
  wallet_transactions_per_minute: number;
};

export type FeatureFlag = {
  name: string;
  enabled: boolean;
  created_at: string;
};


export type FinalizationHealthCheck = {
  name: string;
  healthy: boolean;
  detail: string;
};

export type FinalizationReadiness = {
  capability_areas: string[];
  total_capability_areas: number;
  health_checks: FinalizationHealthCheck[];
  healthy_checks: number;
  readiness_score: number;
  status: 'ready_for_go_live' | 'needs_hardening';
};
