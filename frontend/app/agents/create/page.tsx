'use client';

import { FormEvent, useState } from 'react';

const strategies = ['grid_trading', 'momentum', 'arbitrage', 'ai_trader'];

export default function CreateAgentPage() {
  const [message, setMessage] = useState('');

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const payload = {
      name: formData.get('name'),
      description: formData.get('description'),
      strategy_type: formData.get('strategy_type'),
      initial_capital: Number(formData.get('initial_capital')),
    };
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api/v1'}/agents/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token') ?? ''}`,
      },
      body: JSON.stringify(payload),
    });
    setMessage(response.ok ? 'Agent created successfully' : `Failed: ${response.status}`);
  }

  return (
    <section className="max-w-xl space-y-4">
      <h2 className="text-2xl font-semibold">Create Agent</h2>
      <form onSubmit={onSubmit} className="space-y-3 rounded border border-slate-800 bg-slate-900 p-4">
        <input name="name" placeholder="Name" className="w-full rounded bg-slate-800 p-2" required />
        <textarea name="description" placeholder="Description" className="w-full rounded bg-slate-800 p-2" />
        <select name="strategy_type" className="w-full rounded bg-slate-800 p-2" defaultValue={strategies[0]}>
          {strategies.map((strategy) => (
            <option key={strategy}>{strategy}</option>
          ))}
        </select>
        <input name="initial_capital" type="number" min="1" step="0.01" placeholder="Initial capital" className="w-full rounded bg-slate-800 p-2" required />
        <button className="rounded bg-cyan-500 px-3 py-2 font-medium text-slate-950">Create</button>
      </form>
      {message && <p className="text-sm text-slate-300">{message}</p>}
    </section>
  );
}
