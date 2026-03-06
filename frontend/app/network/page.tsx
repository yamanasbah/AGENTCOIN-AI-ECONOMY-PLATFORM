import Link from 'next/link';

export default function NetworkPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">AI Agent Network</h1>
      <p className="text-zinc-300">Discover agents, build multi-agent workflows, and monitor active collaborations.</p>

      <div className="grid gap-4 md:grid-cols-3">
        <Link href="/network/agents" className="rounded-lg border border-zinc-700 bg-zinc-900 p-4 hover:border-emerald-400">
          <h2 className="text-lg font-semibold">Discover Agents</h2>
          <p className="mt-2 text-sm text-zinc-400">Search by capability, then rank by rating or cost to hire the best fit.</p>
        </Link>
        <Link href="/network/workflows" className="rounded-lg border border-zinc-700 bg-zinc-900 p-4 hover:border-emerald-400">
          <h2 className="text-lg font-semibold">Create Workflows</h2>
          <p className="mt-2 text-sm text-zinc-400">Chain research, analysis, and reporting agents into a collaboration pipeline.</p>
        </Link>
        <div className="rounded-lg border border-zinc-700 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold">Monitor Contracts</h2>
          <p className="mt-2 text-sm text-zinc-400">Track contract statuses: created, accepted, running, completed, or failed.</p>
        </div>
      </div>
    </div>
  );
}
