'use client';

import { useAdminAnalytics } from '@/hooks/use-platform';

export default function AdminAnalyticsPage() {
  const { data } = useAdminAnalytics();

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold text-white">Platform Analytics</h1>
      <pre className="overflow-auto rounded border border-zinc-700 bg-zinc-900 p-4 text-sm text-zinc-300">{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
