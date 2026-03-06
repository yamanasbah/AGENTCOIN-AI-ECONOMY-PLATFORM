'use client';

import { useState } from 'react';
import { useStake, useStaking, useUnstake } from '@/hooks/use-platform';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

export default function StakingPage() {
  const { data } = useStaking();
  const stake = useStake();
  const unstake = useUnstake();
  const [amount, setAmount] = useState('');

  return (
    <Card className="max-w-2xl">
      <CardHeader>
        <CardTitle>Staking</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p>Locked tokens: <span className="text-emerald-400">{data?.locked_tokens ?? 0} AGC</span></p>
        <p>Unlock time: <span className="text-purple-400">{data?.unlock_time ?? '-'}</span></p>
        <Input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="Amount" />
        <div className="flex gap-2">
          <Button onClick={() => stake.mutate(Number(amount))}>Stake Tokens</Button>
          <Button variant="secondary" onClick={() => unstake.mutate(Number(amount))}>Unstake Tokens</Button>
        </div>
      </CardContent>
    </Card>
  );
}
