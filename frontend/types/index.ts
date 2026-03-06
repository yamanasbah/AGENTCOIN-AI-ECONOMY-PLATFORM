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
