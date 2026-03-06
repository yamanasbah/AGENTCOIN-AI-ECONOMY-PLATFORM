'use client';

import { AgentRunner } from '@/components/agent-runner';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useAgent } from '@/hooks/use-platform';

export default function AgentDetailPage({ params }: { params: { id: string } }) {
  const { data: agent } = useAgent(params.id);

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Agent Configuration</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p><span className="text-zinc-400">Name:</span> {agent?.name}</p>
          <p><span className="text-zinc-400">Type:</span> {agent?.type}</p>
          <p><span className="text-zinc-400">Status:</span> {agent?.status}</p>
          <p><span className="text-zinc-400">Execution cost:</span> {agent?.execution_cost ?? 0} AGC</p>
          <p><span className="text-zinc-400">Tools:</span> {agent?.tools?.join(', ') || '-'}</p>
        </CardContent>
      </Card>

      <AgentRunner agentId={params.id} />

      <Card className="lg:col-span-2">
        <CardHeader><CardTitle>Execution History</CardTitle></CardHeader>
        <CardContent>
          <p className="text-sm text-zinc-400">Execution logs are available from backend history endpoints and can be wired here.</p>
        </CardContent>
      </Card>
    </div>
  );
}
