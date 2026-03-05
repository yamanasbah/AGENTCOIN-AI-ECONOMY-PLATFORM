'use client';

import { FormEvent, useState } from 'react';

export default function TokenPage() {
  const [message, setMessage] = useState('');

  async function stake(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const body = { amount: Number(formData.get('amount')), reward_rate: 0.08 };
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api/v1'}/token/stake`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token') ?? ''}` },
      body: JSON.stringify(body),
    });
    setMessage(response.ok ? 'Staked successfully' : 'Stake failed');
  }

  return (
    <section className="max-w-md space-y-4">
      <h2 className="text-2xl font-semibold">AGC Token</h2>
      <form onSubmit={stake} className="space-y-3 rounded border border-slate-800 bg-slate-900 p-4">
        <input name="amount" type="number" min="1" step="0.01" className="w-full rounded bg-slate-800 p-2" placeholder="Stake amount" required />
        <button className="rounded bg-cyan-500 px-3 py-2 font-medium text-slate-950">Stake</button>
      </form>
      {message && <p className="text-sm text-slate-300">{message}</p>}
    </section>
  );
}
