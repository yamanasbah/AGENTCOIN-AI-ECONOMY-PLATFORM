'use client';

import { MarketplaceCard } from '@/components/marketplace-card';
import { useMarketplace } from '@/hooks/use-platform';

export default function MarketplacePage() {
  const { data: agents = [] } = useMarketplace();

  return (
    <div>
      <h2 className="mb-4 text-2xl font-semibold">Marketplace</h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {agents.map((agent) => (
          <MarketplaceCard key={agent.id} agent={agent} />
        ))}
      </div>
    </div>
  );
}
