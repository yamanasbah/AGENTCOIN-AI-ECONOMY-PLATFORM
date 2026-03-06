'use client';

import { useMemo, useState } from 'react';
import { useAgents, useRunAgentRuntime, useRuntimeLogs } from '@/hooks/use-platform';

export default function RunAgentsPage() {
  const { data: agents = [] } = useAgents();
  const [selectedAgentId, setSelectedAgentId] = useState('');
  const [input, setInput] = useState('');
  const [runStatus, setRunStatus] = useState('');
  const runRuntime = useRunAgentRuntime();

  const effectiveAgentId = useMemo(() => selectedAgentId || agents[0]?.id || '', [selectedAgentId, agents]);
  const { data: logs = [], refetch } = useRuntimeLogs(effectiveAgentId);

  const onRun = async () => {
    if (!effectiveAgentId || !input.trim()) return;
    const res = await runRuntime.mutateAsync({ agentId: effectiveAgentId, input: input.trim() });
    setRunStatus(`Task queued: ${res.task_id}`);
    setInput('');
    setTimeout(() => {
      void refetch();
    }, 1500);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Run Agent Runtime</h2>

      <div className="rounded-lg border border-zinc-800 p-4 space-y-3">
        <label className="text-sm text-zinc-300">Select Agent</label>
        <select
          className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2"
          value={effectiveAgentId}
          onChange={(e) => setSelectedAgentId(e.target.value)}
        >
          <option value="">-- Select an agent --</option>
          {agents.map((agent) => (
            <option key={agent.id} value={agent.id}>{agent.name}</option>
          ))}
        </select>

        <label className="text-sm text-zinc-300">Task</label>
        <textarea
          className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe the task for this agent"
          rows={4}
        />

        <button
          className="rounded-md bg-emerald-500 px-4 py-2 font-medium text-black disabled:opacity-60"
          onClick={onRun}
          disabled={runRuntime.isPending}
        >
          {runRuntime.isPending ? 'Running...' : 'Run Agent'}
        </button>

        {runStatus && <p className="text-sm text-emerald-400">{runStatus}</p>}
      </div>

      <div className="rounded-lg border border-zinc-800 p-4">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-lg font-medium">Execution Logs</h3>
          <button className="rounded border border-zinc-700 px-2 py-1 text-xs" onClick={() => refetch()}>Refresh</button>
        </div>
        <div className="space-y-3">
          {logs.length === 0 && <p className="text-sm text-zinc-400">No runtime logs yet.</p>}
          {logs.map((log) => (
            <div key={log.id} className="rounded-md border border-zinc-800 bg-zinc-950 p-3 text-sm">
              <p className="text-zinc-400">{new Date(log.created_at).toLocaleString()} · {log.status}</p>
              <p><span className="text-zinc-400">Input:</span> {log.input_text}</p>
              <p><span className="text-zinc-400">Output:</span> {log.output_text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
