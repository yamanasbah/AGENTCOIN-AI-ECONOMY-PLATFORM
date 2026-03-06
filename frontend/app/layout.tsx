import type { Metadata } from 'next';
import './globals.css';
import { Providers } from '@/components/providers';
import { SiteNav } from '@/components/site-nav';

export const metadata: Metadata = {
  title: 'AgentCoin Platform',
  description: 'AI agent economy dashboard',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-black text-zinc-100">
        <Providers>
          <main className="mx-auto min-h-screen max-w-7xl px-6 py-8">
            <div className="mb-6">
              <h1 className="text-3xl font-bold text-emerald-400">AgentCoin AI Economy</h1>
              <p className="text-zinc-400">Dark-mode AI SaaS + marketplace + AGC wallet.</p>
            </div>
            <SiteNav />
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
