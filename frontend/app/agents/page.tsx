const templates = ['Trading Agent', 'Marketing Agent', 'Arbitrage Agent', 'Social Growth Agent', 'Custom Template'];

export default function AgentsPage() {
  return (
    <section>
      <h2 className="text-2xl font-semibold">Multi-Agent Factory</h2>
      <p className="mb-4 text-slate-300">Create configurable runtime instances with risk + staking controls.</p>
      <div className="grid gap-3 md:grid-cols-2">
        {templates.map((template) => (
          <div key={template} className="rounded-lg border border-slate-800 bg-slate-900 p-4">
            <h3 className="font-medium">{template}</h3>
            <ul className="mt-2 text-sm text-slate-400">
              <li>• Risk configuration</li>
              <li>• Budget allocation</li>
              <li>• Max drawdown + safe mode hooks</li>
              <li>• Token staking requirement</li>
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}
