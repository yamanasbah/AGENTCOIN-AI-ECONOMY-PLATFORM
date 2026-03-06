'use client';

import { MarketplaceAgent } from '@/types';
import { useBuyAgent } from '@/hooks/use-platform';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export function MarketplaceCard({ agent }: { agent: MarketplaceAgent }) {
  const buyMutation = useBuyAgent();

  return (
    <Card>
      <CardHeader>
        <CardTitle>{agent.name}</CardTitle>
        <CardDescription>{agent.description}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-2 text-sm text-zinc-300">
        <p>Price / run: <span className="text-emerald-400">{agent.price_per_run} AGC</span></p>
        <p>Rating: {agent.rating}</p>
        <p>Usage: {agent.usage_count}</p>
        <Button onClick={() => buyMutation.mutate(agent.id)} className="mt-2">Buy / Run</Button>
      </CardContent>
    </Card>
  );
}
