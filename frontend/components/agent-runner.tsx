'use client';

import { useState } from 'react';
import { useRunAgent } from '@/hooks/use-platform';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';

export function AgentRunner({ agentId }: { agentId: string }) {
  const [prompt, setPrompt] = useState('');
  const [messages, setMessages] = useState<{ role: 'user' | 'agent'; content: string }[]>([]);
  const runMutation = useRunAgent(agentId);

  const run = async () => {
    if (!prompt.trim()) return;
    setMessages((prev) => [...prev, { role: 'user', content: prompt }]);
    const current = prompt;
    setPrompt('');
    const result = await runMutation.mutateAsync(current);
    setMessages((prev) => [...prev, { role: 'agent', content: result.output ?? 'Execution completed.' }]);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Run Interface</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="max-h-72 space-y-2 overflow-y-auto rounded-lg border border-zinc-800 p-3">
          {messages.length === 0 && <p className="text-sm text-zinc-500">No messages yet.</p>}
          {messages.map((msg, idx) => (
            <div key={idx} className={`rounded-md p-2 text-sm ${msg.role === 'user' ? 'bg-purple-600/20' : 'bg-emerald-500/20'}`}>
              <p className="mb-1 text-xs uppercase text-zinc-400">{msg.role}</p>
              <p>{msg.content}</p>
            </div>
          ))}
        </div>
        <Textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Send instruction to agent..." />
        <Button onClick={run} disabled={runMutation.isPending}>{runMutation.isPending ? 'Running...' : 'Send & Run'}</Button>
      </CardContent>
    </Card>
  );
}
