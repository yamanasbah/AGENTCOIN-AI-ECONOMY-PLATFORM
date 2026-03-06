const workflowPreview = [
  { order: 1, agent: 'Research Agent', prompt: 'Collect latest market signals and headlines.' },
  { order: 2, agent: 'Data Analysis Agent', prompt: 'Analyze findings and identify high-confidence trends.' },
  { order: 3, agent: 'Report Writing Agent', prompt: 'Generate executive summary and action plan.' },
];

export default function NetworkWorkflowsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Network / Workflows</h1>
        <p className="text-zinc-300">Create and monitor multi-agent collaboration pipelines.</p>
      </div>

      <div className="rounded-lg border border-zinc-700 bg-zinc-900 p-4">
        <h2 className="text-lg font-semibold">Workflow Example</h2>
        <p className="mt-1 text-sm text-zinc-400">Research → Analysis → Reporting</p>
      </div>

      <div className="space-y-3">
        {workflowPreview.map((step) => (
          <div key={step.order} className="rounded-lg border border-zinc-700 bg-zinc-900 p-4">
            <p className="text-sm text-emerald-400">Step {step.order}</p>
            <h3 className="text-lg font-semibold">{step.agent}</h3>
            <p className="text-sm text-zinc-300">{step.prompt}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
