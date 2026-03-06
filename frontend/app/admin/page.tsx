'use client';

import Link from 'next/link';
import { useAdminAnalytics, useRevenueSummary, useSystemHealth } from '@/hooks/use-platform';

export default function AdminPage() {
  const { data: analytics } = useAdminAnalytics();
  const { data: revenue } = useRevenueSummary();
  const { data: health } = useSystemHealth();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-white">Platform Control Center</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded border border-zinc-700 bg-zinc-900 p-4">
          <p className="text-xs text-zinc-400">Total Users</p>
          <p className="text-2xl text-emerald-400">{analytics?.total_users ?? '-'}</p>
        </div>
        <div className="rounded border border-zinc-700 bg-zinc-900 p-4">
          <p className="text-xs text-zinc-400">Total Agents</p>
          <p className="text-2xl text-emerald-400">{analytics?.total_agents ?? '-'}</p>
        </div>
        <div className="rounded border border-zinc-700 bg-zinc-900 p-4">
          <p className="text-xs text-zinc-400">Platform Revenue</p>
          <p className="text-2xl text-emerald-400">{revenue?.platform_revenue ?? '-'}</p>
        </div>
        <div className="rounded border border-zinc-700 bg-zinc-900 p-4">
          <p className="text-xs text-zinc-400">API Latency (ms)</p>
          <p className="text-2xl text-cyan-400">{health?.api_latency_ms ?? '-'}</p>
        </div>
        <div className="rounded border border-zinc-700 bg-zinc-900 p-4">
          <p className="text-xs text-zinc-400">Queue Size</p>
          <p className="text-2xl text-cyan-400">{health?.queue_size ?? '-'}</p>
        </div>
        <div className="rounded border border-zinc-700 bg-zinc-900 p-4">
          <p className="text-xs text-zinc-400">Net Revenue</p>
          <p className="text-2xl text-cyan-400">{revenue?.net_revenue ?? '-'}</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-3 text-sm">
        <Link href="/admin/agents" className="rounded border border-zinc-700 px-3 py-2 text-zinc-200 hover:border-emerald-400">Moderate Agents</Link>
        <Link href="/admin/analytics" className="rounded border border-zinc-700 px-3 py-2 text-zinc-200 hover:border-emerald-400">Analytics</Link>
        <Link href="/admin/treasury" className="rounded border border-zinc-700 px-3 py-2 text-zinc-200 hover:border-emerald-400">Treasury</Link>
        <Link href="/admin/system" className="rounded border border-zinc-700 px-3 py-2 text-zinc-200 hover:border-emerald-400">System Health</Link>
      </div>
    </div>
  );
}
