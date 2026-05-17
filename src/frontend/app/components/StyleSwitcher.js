"use client";

import { useState, useRef, useEffect } from "react";
import { useTheme } from "@/app/providers/ThemeProvider";

const THEME_META = {
  neubrutalism: {
    label: "Neubrutalism",
    icon: "⬛",
    description: "Bold, loud, confident",
  },
  minimalism: {
    label: "Minimalism",
    icon: "○",
    description: "Clean, quiet, elegant",
  },
  neumorphism: {
    label: "Neumorphism",
    icon: "◉",
    description: "Soft, tactile, extruded",
  },
};

export default function StyleSwitcher() {
  const { theme, setTheme, themes } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const wrapperRef = useRef(null);

  // Close on click outside
  useEffect(() => {
    function handleClickOutside(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Close on Escape
  useEffect(() => {
    function handleEscape(e) {
      if (e.key === "Escape") setIsOpen(false);
    }
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, []);

  const current = THEME_META[theme];

  return (
    <div className="dropdown-wrapper" ref={wrapperRef}>
      <button
        className="dropdown-trigger"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        id="style-switcher-trigger"
      >
        {current.label}
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="none"
          style={{
            transform: isOpen ? "rotate(180deg)" : "rotate(0deg)",
            transition: "transform 0.2s ease",
          }}
        >
          <path
            d="M2.5 4.5L6 8L9.5 4.5"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      <div
        className={`dropdown-menu premium-glass ${isOpen ? "open" : ""}`}
        role="listbox"
        aria-labelledby="style-switcher-trigger"
      >
        {themes.map((t) => {
          const meta = THEME_META[t];
          return (
            <button
              key={t}
              className={`dropdown-item ${theme === t ? "active" : ""}`}
              onClick={() => {
                setTheme(t);
                setIsOpen(false);
              }}
              role="option"
              aria-selected={theme === t}
              id={`theme-option-${t}`}
            >
              <div style={{ fontWeight: 600 }}>{meta.label}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
