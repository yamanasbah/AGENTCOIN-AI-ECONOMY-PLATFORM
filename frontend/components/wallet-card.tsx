'use client';

import { useState } from 'react';
import { useTransfer } from '@/hooks/use-platform';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

export function WalletCard() {
  const [to, setTo] = useState('');
  const [amount, setAmount] = useState('');
  const transfer = useTransfer();

  return (
    <Card>
      <CardHeader>
        <CardTitle>Transfer AGC</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <Input placeholder="Recipient wallet" value={to} onChange={(e) => setTo(e.target.value)} />
        <Input type="number" placeholder="Amount" value={amount} onChange={(e) => setAmount(e.target.value)} />
        <Button onClick={() => transfer.mutate({ to, amount: Number(amount) })} disabled={transfer.isPending}>
          {transfer.isPending ? 'Transferring...' : 'Transfer'}
        </Button>
      </CardContent>
    </Card>
  );
}
