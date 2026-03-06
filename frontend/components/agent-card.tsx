import Link from 'next/link';
import { Agent } from '@/types';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export function AgentCard({ agent, onRun }: { agent: Agent; onRun?: () => void }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{agent.name}</CardTitle>
        <CardDescription>
          {agent.type} · {agent.status}
        </CardDescription>
      </CardHeader>
      <CardContent className="flex items-center justify-between">
        <p className="text-sm text-zinc-400">Runs: {agent.runs}</p>
        <div className="flex gap-2">
          <Button size="sm" onClick={onRun}>
            Run
          </Button>
          <Link href={`/agents/${agent.id}`} className="inline-flex h-9 items-center rounded-md border border-zinc-700 bg-zinc-900 px-3 text-sm text-zinc-100">
            Details
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
