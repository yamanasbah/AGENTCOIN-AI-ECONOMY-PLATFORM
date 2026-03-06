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
