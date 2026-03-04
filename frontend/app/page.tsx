import { MetricCard } from '@/components/metric-card';

export default function HomePage() {
  return (
    <section className="space-y-6">
      <h1 className="text-3xl font-bold">AgentCoin AI Economy</h1>
      <p className="text-slate-300">Production-ready AI Agent creation and monetization infrastructure.</p>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
        <MetricCard title="Active Agents" value="517" />
        <MetricCard title="Token Staked" value="125,000 AGC" />
        <MetricCard title="Monthly Commission" value="2,100 AGC" />
        <MetricCard title="Marketplace Listings" value="184" />
      </div>
    </section>
  );
}
