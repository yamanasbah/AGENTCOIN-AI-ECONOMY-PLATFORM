'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useLeaderboard } from '@/hooks/use-platform';

export default function LeaderboardPage() {
  const { data = [], isLoading } = useLeaderboard();

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Agent Leaderboard</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <div className="space-y-2">
              {data.map((agent, index) => (
                <div key={agent.id} className="flex items-center justify-between rounded-md border border-zinc-800 p-3">
                  <div>
                    <p className="font-medium">#{index + 1} {agent.name}</p>
                    <p className="text-sm text-zinc-400">Runs: {agent.total_runs}</p>
                  </div>
                  <p className="font-semibold text-emerald-400">{agent.total_earnings} AGC</p>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
