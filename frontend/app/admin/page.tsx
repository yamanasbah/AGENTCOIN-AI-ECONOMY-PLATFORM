export default function AdminPage() {
  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-semibold">Admin Control Plane</h2>
      <div className="rounded-lg border border-slate-800 bg-slate-900 p-4 text-slate-300">
        <p>Track token usage, revenue analytics, agent growth, and global risk controls.</p>
        <ul className="mt-3 text-sm text-slate-400">
          <li>• Force safe mode</li>
          <li>• Adjust max global drawdown</li>
          <li>• Audit operational events</li>
        </ul>
      </div>
    </section>
  );
}
