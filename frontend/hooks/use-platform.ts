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


export function useLeaderboard() {
  return useQueryState(API.getAgentLeaderboard, []);
}

export function useCreatorStats() {
  return useQueryState(API.getCreatorStats, []);
}


export function useNotifications() {
  return useQueryState(API.getNotifications, []);
}

export function useReadNotification() {
  return useMutationState(API.readNotification);
}

export function useAnalytics() {
  return useQueryState(API.getPlatformAnalytics, []);
}

export function useApiKeys() {
  return useQueryState(API.getApiKeys, []);
}

export function useCreateApiKey() {
  return useMutationState(API.createApiKey);
}

export function useDeleteApiKey() {
  return useMutationState(API.deleteApiKey);
}


export function useStoreAgents(params?: { category?: string; price?: number; rating?: number; popularity?: string }) {
  return useQueryState(() => API.getStoreAgents(params), [JSON.stringify(params || {})]);
}

export function useStoreAgent(id: string) {
  return useQueryState(() => API.getStoreAgent(id), [id]);
}

export function useInstallStoreAgent() {
  return useMutationState(API.installStoreAgent);
}

export function useMyInstalledAgents() {
  return useQueryState(API.getMyInstalledAgents, []);
}

export function useReviewStoreAgent() {
  return useMutationState(API.reviewStoreAgent);
}

export function useStoreReviews(agentId: string) {
  return useQueryState(() => (agentId ? API.getStoreReviews(agentId) : Promise.resolve([])), [agentId]);
}

export function usePublishAgent() {
  return useMutationState(({ id, payload }: { id: string; payload: { title?: string; description?: string; category: string; tags: string[]; price_per_run: number; price_per_month: number } }) => API.publishAgent(id, payload));
}

export function useAdminAnalytics() {
  return useQueryState(API.getAdminAnalytics, []);
}

export function useAdminTreasury() {
  return useQueryState(API.getAdminTreasury, []);
}

export function useRevenueSummary() {
  return useQueryState(API.getRevenueSummary, []);
}

export function usePendingAgents() {
  return useQueryState(API.getPendingAgents, []);
}

export function useAgentFlags() {
  return useQueryState(API.getAgentFlags, []);
}

export function useSystemHealth() {
  return useQueryState(API.getSystemHealth, []);
}

export function useFeatureFlags() {
  return useQueryState(API.getFeatures, []);
}

export function useApproveAgent(onSuccess?: () => void) {
  return useMutationState(API.approveAgent, onSuccess);
}

export function useRejectAgent(onSuccess?: () => void) {
  return useMutationState(API.rejectAgent, onSuccess);
}

export function useBanAgent(onSuccess?: () => void) {
  return useMutationState(API.banAgent, onSuccess);
}

export function useUpdateFeatureFlag(onSuccess?: () => void) {
  return useMutationState(({ name, enabled }: { name: string; enabled: boolean }) => API.updateFeatureFlag(name, enabled), onSuccess);
}


export function useFinalizationReadiness() {
  return useQueryState(API.getFinalizationReadiness, []);
}
