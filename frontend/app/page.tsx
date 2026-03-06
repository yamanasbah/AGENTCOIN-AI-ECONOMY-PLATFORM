'use client';

import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAgents, useMarketplace, useWallet } from '@/hooks/use-platform';

export default function DashboardPage() {
  const { data: agents = [] } = useAgents();
  const { data: wallet } = useWallet();
  const { data: marketplace = [] } = useMarketplace();

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card><CardHeader><CardDescription>Total Agents</CardDescription><CardTitle>{agents.length}</CardTitle></CardHeader></Card>
        <Card><CardHeader><CardDescription>Wallet Balance</CardDescription><CardTitle>{wallet?.balance ?? 0} AGC</CardTitle></CardHeader></Card>
        <Card><CardHeader><CardDescription>Recent Executions</CardDescription><CardTitle>{agents.reduce((a, b) => a + (b.runs || 0), 0)}</CardTitle></CardHeader></Card>
        <Card><CardHeader><CardDescription>Marketplace Highlights</CardDescription><CardTitle>{marketplace.length}</CardTitle></CardHeader></Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-3">
          <Link href="/agents/create" className="rounded-md bg-emerald-500 px-4 py-2 font-medium text-black">Create Agent</Link>
          <Link href="/marketplace" className="rounded-md border border-zinc-700 bg-zinc-900 px-4 py-2">Open Marketplace</Link>
        </CardContent>
      </Card>
    </div>
  );
}
