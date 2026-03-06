'use client';

import Link from 'next/link';
import { useAgents, useDeleteAgent, useRunAgent } from '@/hooks/use-platform';
import { Button } from '@/components/ui/button';

export default function AgentsPage() {
  const { data: agents = [] } = useAgents();
  const del = useDeleteAgent();

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">My Agents</h2>
        <Link href="/agents/create" className="rounded-md bg-emerald-500 px-4 py-2 font-medium text-black">Create Agent</Link>
      </div>
      <div className="overflow-x-auto rounded-lg border border-zinc-800">
        <table className="w-full text-left text-sm">
          <thead className="bg-zinc-900 text-zinc-300">
            <tr>
              <th className="p-3">Name</th><th className="p-3">Type</th><th className="p-3">Status</th><th className="p-3">Runs</th><th className="p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((agent) => (
              <AgentRow key={agent.id} agent={agent} onDelete={() => del.mutate(agent.id)} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function AgentRow({ agent, onDelete }: { agent: { id: string; name: string; type: string; status: string; runs: number }, onDelete: () => void }) {
  const run = useRunAgent(agent.id);

  return (
    <tr className="border-t border-zinc-800">
      <td className="p-3">{agent.name}</td>
      <td className="p-3">{agent.type}</td>
      <td className="p-3">{agent.status}</td>
      <td className="p-3">{agent.runs}</td>
      <td className="p-3">
        <div className="flex gap-2">
          <Button size="sm" onClick={() => run.mutate('Quick run from table')}>Run Agent</Button>
          <Link className="rounded-md border border-zinc-700 px-3 py-1 text-xs" href={`/agents/${agent.id}`}>Edit</Link>
          <Button variant="destructive" size="sm" onClick={onDelete}>Delete</Button>
        </div>
      </td>
    </tr>
  );
}
