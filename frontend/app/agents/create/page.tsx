'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useCreateAgent } from '@/hooks/use-platform';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function CreateAgentPage() {
  const router = useRouter();
  const create = useCreateAgent();
  const [form, setForm] = useState({
    name: '',
    agent_type: '',
    system_prompt: '',
    tools: '',
    execution_cost: '0',
  });

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await create.mutateAsync({
      ...form,
      tools: form.tools.split(',').map((t) => t.trim()).filter(Boolean),
      execution_cost: Number(form.execution_cost),
    });
    router.push('/agents');
  };

  return (
    <Card className="max-w-2xl">
      <CardHeader><CardTitle>Create Agent</CardTitle></CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-3">
          <Input placeholder="name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <Input placeholder="agent_type" value={form.agent_type} onChange={(e) => setForm({ ...form, agent_type: e.target.value })} required />
          <Textarea placeholder="system_prompt" value={form.system_prompt} onChange={(e) => setForm({ ...form, system_prompt: e.target.value })} required />
          <Input placeholder="tools (comma separated)" value={form.tools} onChange={(e) => setForm({ ...form, tools: e.target.value })} />
          <Input type="number" placeholder="execution_cost" value={form.execution_cost} onChange={(e) => setForm({ ...form, execution_cost: e.target.value })} required />
          <Button type="submit" disabled={create.isPending}>{create.isPending ? 'Creating...' : 'Create Agent'}</Button>
        </form>
      </CardContent>
    </Card>
  );
}
