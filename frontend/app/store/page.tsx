'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useStoreAgents } from '@/hooks/use-platform';

const categories = ['All', 'Marketing', 'Trading', 'Research', 'Content', 'Automation', 'Crypto', 'Productivity'];

export default function StorePage() {
  const [category, setCategory] = useState('All');
  const [popularity, setPopularity] = useState('trending');
  const { data = [] } = useStoreAgents({ category: category === 'All' ? undefined : category, popularity });

  return (
    <div>
      <h2 className="mb-4 text-2xl font-semibold">AI Agent App Store</h2>
      <div className="mb-4 flex gap-3">
        <select className="rounded border bg-zinc-900 p-2" value={category} onChange={(e) => setCategory(e.target.value)}>
          {categories.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <select className="rounded border bg-zinc-900 p-2" value={popularity} onChange={(e) => setPopularity(e.target.value)}>
          <option value="trending">Trending</option>
          <option value="new">New</option>
          <option value="top_rated">Top Rated</option>
        </select>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {data.map((agent) => (
          <Link key={agent.id} href={`/store/agent/${agent.id}`} className="rounded-lg border border-zinc-700 bg-zinc-900 p-4">
            <h3 className="font-semibold">{agent.title}</h3>
            <p className="text-sm text-zinc-400">{agent.description}</p>
            <p className="mt-2 text-sm">⭐ {agent.rating} · Runs: {agent.usage_count}</p>
            <p className="text-sm">{agent.price_per_run} AGC / run</p>
            <p className="text-xs text-zinc-500">By @{agent.creator_username}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
