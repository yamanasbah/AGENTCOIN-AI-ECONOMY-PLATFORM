'use client';

import { useAgentFlags, useApproveAgent, useBanAgent, usePendingAgents, useRejectAgent } from '@/hooks/use-platform';

export default function AdminAgentsPage() {
  const pending = usePendingAgents();
  const flags = useAgentFlags();
  const approve = useApproveAgent(() => pending.refetch());
  const reject = useRejectAgent(() => pending.refetch());
  const ban = useBanAgent(() => pending.refetch());

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-white">Agent Moderation Queue</h1>
      <div className="space-y-3">
        {(pending.data || []).map((agent) => (
          <div key={agent.id} className="rounded border border-zinc-700 bg-zinc-900 p-4">
            <p className="text-sm text-zinc-200">{agent.name}</p>
            <p className="text-xs text-zinc-500">{agent.id}</p>
            <div className="mt-3 flex gap-2">
              <button onClick={() => approve.mutate(agent.id)} className="rounded bg-emerald-600 px-3 py-1 text-xs">Approve</button>
              <button onClick={() => reject.mutate(agent.id)} className="rounded bg-amber-600 px-3 py-1 text-xs">Reject</button>
              <button onClick={() => ban.mutate(agent.id)} className="rounded bg-rose-700 px-3 py-1 text-xs">Ban</button>
            </div>
          </div>
        ))}
      </div>

      <div>
        <h2 className="mb-2 text-lg text-zinc-200">Flagged Agents</h2>
        <div className="space-y-2">
          {(flags.data || []).map((flag) => (
            <div key={`${flag.agent_id}-${flag.reason}`} className="rounded border border-zinc-700 bg-zinc-900 p-3 text-sm">
              <p className="text-zinc-200">{flag.agent_id}</p>
              <p className="text-zinc-400">{flag.reason} ({flag.flag_count})</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
