'use client';

import { useAdminTreasury, useRevenueSummary } from '@/hooks/use-platform';

export default function AdminTreasuryPage() {
  const { data: treasury } = useAdminTreasury();
  const { data: revenue } = useRevenueSummary();

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold text-white">Platform Treasury</h1>
      <pre className="overflow-auto rounded border border-zinc-700 bg-zinc-900 p-4 text-sm text-zinc-300">{JSON.stringify(treasury, null, 2)}</pre>
      <pre className="overflow-auto rounded border border-zinc-700 bg-zinc-900 p-4 text-sm text-zinc-300">{JSON.stringify(revenue, null, 2)}</pre>
    </div>
  );
}
