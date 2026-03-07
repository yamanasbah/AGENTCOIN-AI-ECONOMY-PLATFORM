'use client';

import { useFeatureFlags, useFinalizationReadiness, useSystemHealth, useUpdateFeatureFlag } from '@/hooks/use-platform';

export default function AdminSystemPage() {
  const health = useSystemHealth();
  const features = useFeatureFlags();
  const finalization = useFinalizationReadiness();
  const updateFeature = useUpdateFeatureFlag(() => features.refetch());

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-white">System Health & Feature Flags</h1>
      <pre className="overflow-auto rounded border border-zinc-700 bg-zinc-900 p-4 text-sm text-zinc-300">{JSON.stringify(health.data, null, 2)}</pre>
      <section className="space-y-4 rounded border border-zinc-700 bg-zinc-900 p-4">
        <h2 className="text-lg font-semibold text-white">Mission Finalization Readiness</h2>
        <p className="text-sm text-zinc-300">
          Score: {finalization.data?.readiness_score ?? 0}% · Healthy checks: {finalization.data?.healthy_checks ?? 0}/
          {finalization.data?.health_checks?.length ?? 0} · Status: {finalization.data?.status ?? 'loading'}
        </p>
        <div className="grid gap-2">
          {(finalization.data?.health_checks || []).map((check) => (
            <div key={check.name} className="rounded border border-zinc-700 p-3 text-sm">
              <div className="font-medium text-white">
                {check.healthy ? '✅' : '⚠️'} {check.name}
              </div>
              <div className="text-zinc-400">{check.detail}</div>
            </div>
          ))}
        </div>
        <details className="rounded border border-zinc-700 p-3 text-sm">
          <summary className="cursor-pointer text-zinc-200">Covered platform capability areas</summary>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-zinc-300">
            {(finalization.data?.capability_areas || []).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </details>
      </section>

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
