'use client';

import { useCallback, useEffect, useState } from 'react';
import { API } from '@/services/api';

function useQueryState<T>(fetcher: () => Promise<T>, deps: unknown[] = []) {
  const [data, setData] = useState<T | undefined>();
  const [isLoading, setIsLoading] = useState(true);

  const refetch = useCallback(async () => {
    setIsLoading(true);
    try {
      setData(await fetcher());
    } finally {
      setIsLoading(false);
    }
  }, deps); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { data, isLoading, refetch };
}

function useMutationState<TArgs, TResult>(mutationFn: (args: TArgs) => Promise<TResult>, onSuccess?: () => void) {
  const [isPending, setIsPending] = useState(false);

  const mutateAsync = async (args: TArgs) => {
    setIsPending(true);
    try {
      const result = await mutationFn(args);
      onSuccess?.();
      return result;
    } finally {
      setIsPending(false);
    }
  };

  const mutate = (args: TArgs) => {
    void mutateAsync(args);
  };

  return { mutate, mutateAsync, isPending };
}

export function useAgents() {
  return useQueryState(API.getAgents, []);
}

export function useAgent(id: string) {
  return useQueryState(() => API.getAgent(id), [id]);
}

export function useMarketplace() {
  return useQueryState(API.getMarketplaceAgents, []);
}

export function useWallet() {
  return useQueryState(API.getWalletBalance, []);
}

export function useTransactions() {
  return useQueryState(API.getTransactions, []);
}

export function useStaking() {
  return useQueryState(API.getStaking, []);
}

export function useCreateAgent() {
  return useMutationState(API.createAgent);
}

export function useRunAgent(id: string) {
  return useMutationState((input: string) => API.runAgent(id, input));
}

export function useDeleteAgent() {
  return useMutationState(API.deleteAgent);
}

export function useBuyAgent() {
  return useMutationState(API.buyMarketplaceAgent);
}

export function useTransfer() {
  return useMutationState(({ to, amount }: { to: string; amount: number }) => API.transferWallet(to, amount));
}

export function useStake() {
  return useMutationState(API.stake);
}

export function useUnstake() {
  return useMutationState(API.unstake);
}


export function useRunAgentRuntime() {
  return useMutationState(({ agentId, input }: { agentId: string; input: string }) => API.runAgentRuntime(agentId, input));
}

export function useRuntimeLogs(agentId: string) {
  return useQueryState(() => API.getRuntimeLogs(agentId), [agentId]);
}
