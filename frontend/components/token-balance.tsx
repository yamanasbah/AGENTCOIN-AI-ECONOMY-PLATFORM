import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function TokenBalance({ balance }: { balance: number }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>AGC Balance</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-3xl font-bold text-emerald-400">{balance.toLocaleString()} AGC</p>
      </CardContent>
    </Card>
  );
}
