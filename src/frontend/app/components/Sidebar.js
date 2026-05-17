"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { label: "Dashboard", href: "/", icon: "◒" },
  { label: "Content", href: "/content", icon: "▤" },
  { label: "Schedule", href: "/schedule", icon: "▦" },
  { label: "Analytics", href: "/analytics", icon: "◩" },
  { label: "Agents", href: "/agents", icon: "◈" },
];

export default function Sidebar({ isCollapsed, onToggle }) {
  const pathname = usePathname();

  return (
    <aside className={`sidebar premium-glass ${isCollapsed ? "collapsed" : ""}`} id="main-sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo cursive-brand">
          <span className="sidebar-logo-text">AGS Core</span>
        </div>
        <button className="collapse-btn" onClick={onToggle}>
          {isCollapsed ? "→" : "←"}
        </button>
      </div>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`sidebar-link ${pathname === item.href ? "active" : ""}`}
            title={isCollapsed ? item.label : ""}
          >
            <span style={{ fontSize: "1.2rem", fontWeight: 800 }}>{item.icon}</span>
            <span className="sidebar-link-text">{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}
