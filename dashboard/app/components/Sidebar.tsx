"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", icon: "🏠", label: "Home" },
  { href: "/executive", icon: "📊", label: "Executive Dashboard" },
  { href: "/analytics", icon: "📈", label: "Business Analytics" },
  { href: "/predict", icon: "🤖", label: "ML Prediction" },
  { href: "/decision", icon: "⚖️", label: "Decision Support" },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <nav className="sidebar">
      <div className="sidebar-logo">
        Credit Risk
        <span>Intelligence Platform</span>
      </div>
      {navItems.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={`nav-item ${pathname === item.href ? "active" : ""}`}
        >
          <span className="nav-icon">{item.icon}</span>
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
