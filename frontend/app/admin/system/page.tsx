'use client';

import { useFeatureFlags, useSystemHealth, useUpdateFeatureFlag } from '@/hooks/use-platform';

export default function AdminSystemPage() {
  const health = useSystemHealth();
  const features = useFeatureFlags();
  const updateFeature = useUpdateFeatureFlag(() => features.refetch());

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-white">System Health & Feature Flags</h1>
      <pre className="overflow-auto rounded border border-zinc-700 bg-zinc-900 p-4 text-sm text-zinc-300">{JSON.stringify(health.data, null, 2)}</pre>
      <div className="space-y-2">
        {(features.data || []).map((feature) => (
          <div key={feature.name} className="flex items-center justify-between rounded border border-zinc-700 bg-zinc-900 p-3">
            <span>{feature.name}</span>
            <button
              onClick={() => updateFeature.mutate({ name: feature.name, enabled: !feature.enabled })}
              className="rounded border border-zinc-500 px-3 py-1 text-xs"
            >
              {feature.enabled ? 'Disable' : 'Enable'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
