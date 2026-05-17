"use client";

import { useState } from "react";
import Sidebar from "@/app/components/Sidebar";

export default function WebLayout({ children }) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div className="app-layout">
      <Sidebar isCollapsed={isCollapsed} onToggle={() => setIsCollapsed(!isCollapsed)} />
      <main className={`main-content ${isCollapsed ? "collapsed" : ""}`}>
        {children}
      </main>
    </div>
  );
}
