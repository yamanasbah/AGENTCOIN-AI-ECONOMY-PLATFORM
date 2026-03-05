'use client';

import { useEffect, useState } from 'react';

export default function WalletPage() {
  const [wallet, setWallet] = useState<any>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api/v1'}/wallet`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token') ?? ''}` },
    })
      .then((r) => r.json())
      .then(setWallet)
      .catch(() => setWallet(null));
  }, []);

  return (
    <section>
      <h2 className="text-2xl font-semibold">Wallet</h2>
      <pre className="mt-3 rounded bg-slate-900 p-4 text-sm">{JSON.stringify(wallet, null, 2)}</pre>
    </section>
  );
}
