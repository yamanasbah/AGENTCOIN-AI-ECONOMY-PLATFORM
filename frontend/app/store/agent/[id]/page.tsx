'use client';

import { useParams } from 'next/navigation';
import { useState } from 'react';
import { useInstallStoreAgent, useReviewStoreAgent, useStoreAgent, useStoreReviews } from '@/hooks/use-platform';

export default function StoreAgentDetailPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const { data: agent } = useStoreAgent(id);
  const { data: reviews = [], refetch } = useStoreReviews(agent?.agent_id || '');
  const installMutation = useInstallStoreAgent();
  const reviewMutation = useReviewStoreAgent();
  const [rating, setRating] = useState(5);
  const [review, setReview] = useState('');

  if (!agent) return <div>Loading...</div>;

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">{agent.title}</h2>
      <p>{agent.description}</p>
      <p>Category: {agent.category}</p>
      <p>Price: {agent.price_per_run} AGC/run · {agent.price_per_month} AGC/month</p>
      <p>Rating: ⭐ {agent.rating} · Total runs: {agent.total_runs}</p>
      <button className="rounded bg-emerald-600 px-4 py-2" onClick={() => installMutation.mutate(agent.agent_id)}>
        Install Agent
      </button>

      <div className="rounded border border-zinc-700 p-4">
        <h3 className="mb-2 font-semibold">Leave a Review</h3>
        <input className="mb-2 w-full rounded border bg-zinc-900 p-2" type="number" min={1} max={5} value={rating} onChange={(e) => setRating(Number(e.target.value))} />
        <textarea className="mb-2 w-full rounded border bg-zinc-900 p-2" value={review} onChange={(e) => setReview(e.target.value)} />
        <button
          className="rounded bg-blue-600 px-4 py-2"
          onClick={async () => {
            await reviewMutation.mutateAsync({ agent_id: agent.agent_id, rating, review });
            setReview('');
            refetch();
          }}
        >
          Submit Review
        </button>
      </div>

      <div>
        <h3 className="font-semibold">Reviews</h3>
        <ul className="space-y-2">
          {reviews.map((r) => (
            <li key={r.id} className="rounded border border-zinc-700 p-3">
              <p>⭐ {r.rating}</p>
              <p>{r.review}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
