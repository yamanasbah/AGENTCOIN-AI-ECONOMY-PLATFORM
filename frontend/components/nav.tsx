import Link from 'next/link';

const links = [
  { href: '/', label: 'Overview' },
  { href: '/agents', label: 'Agent Factory' },
  { href: '/agents/create', label: 'Create Agent' },
  { href: '/wallet', label: 'Wallet' },
  { href: '/token', label: 'Token' },
  { href: '/marketplace', label: 'Marketplace' },
  { href: '/dashboard', label: 'Monitoring' },
  { href: '/admin', label: 'Admin' },
];

export function Nav() {
  return (
    <nav className="flex gap-4 border-b border-slate-800 p-4 text-sm">
      {links.map((link) => (
        <Link key={link.href} href={link.href} className="text-slate-300 hover:text-cyan-400">
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
