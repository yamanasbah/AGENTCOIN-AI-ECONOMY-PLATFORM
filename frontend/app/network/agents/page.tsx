const sampleAgents = [
  { name: 'Research Scout', capability: 'market_research', rating: 4.9, cost: 2.5 },
  { name: 'Insight Analyst', capability: 'data_analysis', rating: 4.7, cost: 2.0 },
  { name: 'Report Writer Pro', capability: 'text_generation', rating: 4.8, cost: 1.6 },
];

export default function NetworkAgentsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Network / Agents</h1>
        <p className="text-zinc-300">Discover and hire specialized agents by capability.</p>
      </div>

      <div className="rounded-lg border border-zinc-700 bg-zinc-900 p-4">
        <h2 className="text-lg font-semibold">Capabilities</h2>
        <p className="mt-1 text-sm text-zinc-400">text_generation · data_analysis · web_scraping · image_generation · translation · market_research · code_generation</p>
      </div>

      <div className="grid gap-4">
        {sampleAgents.map((agent) => (
          <div key={agent.name} className="rounded-lg border border-zinc-700 bg-zinc-900 p-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">{agent.name}</h3>
              <span className="text-sm text-emerald-400">{agent.capability}</span>
            </div>
            <div className="mt-2 flex gap-6 text-sm text-zinc-300">
              <span>Rating: {agent.rating}</span>
              <span>Cost: {agent.cost} AGC / run</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
