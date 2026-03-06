'use client';

import { TokenBalance } from '@/components/token-balance';
import { WalletCard } from '@/components/wallet-card';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useTransactions, useWallet } from '@/hooks/use-platform';

export default function WalletPage() {
  const { data: wallet } = useWallet();
  const { data: transactions = [] } = useTransactions();

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <TokenBalance balance={wallet?.balance ?? 0} />
      <WalletCard />
      <Card className="lg:col-span-2">
        <CardHeader><CardTitle>Recent Transactions</CardTitle></CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm">
            {transactions.length === 0 && <p className="text-zinc-400">No recent transactions.</p>}
            {transactions.map((tx) => (
              <div key={tx.id} className="rounded-md border border-zinc-800 p-2">
                <p>{tx.type} · {tx.amount} AGC · {tx.to}</p>
                <p className="text-zinc-500">{tx.created_at}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
