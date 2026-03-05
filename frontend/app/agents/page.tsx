import Link from 'next/link';

export default function AgentsPage() {
  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-semibold">Agent Factory</h2>
      <p className="text-slate-300">Create and manage automated AI agents.</p>
      <Link href="/agents/create" className="inline-block rounded bg-cyan-500 px-4 py-2 text-slate-950">Create Agent</Link>
    </section>
  );
}
