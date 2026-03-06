import Link from 'next/link';

const links = [
  { href: '/', label: 'Dashboard' },
  { href: '/agents', label: 'Agents' },
  { href: '/agents/run', label: 'Run Agent' },
  { href: '/marketplace', label: 'Marketplace' },
  { href: '/wallet', label: 'Wallet' },
  { href: '/staking', label: 'Staking' },
];

export function SiteNav() {
  return (
    <nav className="mb-8 flex flex-wrap gap-2">
      {links.map((link) => (
        <Link key={link.href} href={link.href} className="rounded-md border border-zinc-700 bg-zinc-900 px-4 py-2 text-sm text-zinc-200 hover:border-emerald-400">
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
