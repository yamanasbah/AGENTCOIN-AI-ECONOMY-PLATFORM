'use client';

import { FormEvent, useState } from 'react';
import { useAgents, usePublishAgent } from '@/hooks/use-platform';

const categories = ['Marketing', 'Trading', 'Research', 'Content', 'Automation', 'Crypto', 'Productivity'];

export default function PublishAgentPage() {
  const { data: agents = [] } = useAgents();
  const publishMutation = usePublishAgent();
  const [agentId, setAgentId] = useState('');
  const [category, setCategory] = useState('Marketing');
  const [pricePerRun, setPricePerRun] = useState(1);
  const [pricePerMonth, setPricePerMonth] = useState(20);
  const [tags, setTags] = useState('');

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!agentId) return;
    await publishMutation.mutateAsync({
      id: agentId,
      payload: {
        category,
        tags: tags.split(',').map((t) => t.trim()).filter(Boolean),
        price_per_run: pricePerRun,
        price_per_month: pricePerMonth,
      },
    });
  };

  return (
    <div>
      <h2 className="mb-4 text-2xl font-semibold">Publish Agent</h2>
      <form onSubmit={onSubmit} className="max-w-xl space-y-3">
        <select className="w-full rounded border bg-zinc-900 p-2" value={agentId} onChange={(e) => setAgentId(e.target.value)}>
          <option value="">Select your agent</option>
          {agents.map((agent) => <option key={agent.id} value={agent.id}>{agent.name}</option>)}
        </select>
        <select className="w-full rounded border bg-zinc-900 p-2" value={category} onChange={(e) => setCategory(e.target.value)}>
          {categories.map((cat) => <option key={cat} value={cat}>{cat}</option>)}
        </select>
        <input className="w-full rounded border bg-zinc-900 p-2" type="number" step="0.0001" value={pricePerRun} onChange={(e) => setPricePerRun(Number(e.target.value))} placeholder="Price per run" />
        <input className="w-full rounded border bg-zinc-900 p-2" type="number" step="0.0001" value={pricePerMonth} onChange={(e) => setPricePerMonth(Number(e.target.value))} placeholder="Price per month" />
        <input className="w-full rounded border bg-zinc-900 p-2" value={tags} onChange={(e) => setTags(e.target.value)} placeholder="tags,comma,separated" />
        <button className="rounded bg-emerald-600 px-4 py-2" type="submit">Publish</button>
      </form>
    </div>
  );
}
