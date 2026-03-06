'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useCreatorStats } from '@/hooks/use-platform';

export default function CreatorPage() {
  const { data, isLoading } = useCreatorStats();

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Creator Analytics</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <div className="grid gap-3 md:grid-cols-3">
              <div className="rounded-md border border-zinc-800 p-3">
                <p className="text-sm text-zinc-400">Total Agents</p>
                <p className="text-xl font-semibold">{data?.total_agents ?? 0}</p>
              </div>
              <div className="rounded-md border border-zinc-800 p-3">
                <p className="text-sm text-zinc-400">Total Earnings</p>
                <p className="text-xl font-semibold text-emerald-400">{data?.total_earnings ?? 0} AGC</p>
              </div>
              <div className="rounded-md border border-zinc-800 p-3">
                <p className="text-sm text-zinc-400">Total Runs</p>
                <p className="text-xl font-semibold">{data?.total_runs ?? 0}</p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
