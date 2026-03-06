import Link from 'next/link';

const links = [
  { href: '/', label: 'Overview' },
  { href: '/agents', label: 'Agent Factory' },
  { href: '/agents/create', label: 'Create Agent' },
  { href: '/wallet', label: 'Wallet' },
  { href: '/token', label: 'Token' },
  { href: '/marketplace', label: 'Marketplace' },
  { href: '/leaderboard', label: 'Leaderboard' },
  { href: '/creator', label: 'Creator' },
  { href: '/dashboard', label: 'Monitoring' },
  { href: '/admin', label: 'Admin' },
  { href: '/login', label: 'Login' },
  { href: '/register', label: 'Register' },
  { href: '/api-keys', label: 'API Keys' },
  { href: '/notifications', label: 'Notifications' },
  { href: '/analytics', label: 'Analytics' },
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
