import { PerformanceChart } from '@/components/performance-chart';

export default function DashboardPage() {
  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-semibold">Real-time Monitoring</h2>
      <p className="text-slate-300">WebSocket channels: balances, trade feed, safe mode alerts, staking updates.</p>
      <PerformanceChart />
    </section>
  );
}
