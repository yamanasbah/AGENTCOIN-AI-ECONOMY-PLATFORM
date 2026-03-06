'use client';

import { useMyInstalledAgents } from '@/hooks/use-platform';

export default function MyAgentsPage() {
  const { data = [] } = useMyInstalledAgents();

  return (
    <div>
      <h2 className="mb-4 text-2xl font-semibold">My Installed Agents</h2>
      <ul className="space-y-2">
        {data.map((agent) => (
          <li key={agent.id} className="rounded border border-zinc-700 bg-zinc-900 p-3">
            <p>Agent ID: {agent.agent_id}</p>
            <p>Installed: {new Date(agent.installed_at).toLocaleString()}</p>
            <p>Status: {agent.active ? 'Active' : 'Inactive'}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
