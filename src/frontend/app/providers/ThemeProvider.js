"use client";

import { createContext, useContext, useState, useEffect, useCallback } from "react";

const THEMES = ["neubrutalism", "minimalism", "neumorphism"];
const STORAGE_KEY = "ags-theme";
const DEFAULT_THEME = "neubrutalism";

const ThemeContext = createContext({
  theme: DEFAULT_THEME,
  setTheme: () => {},
  themes: THEMES,
});

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(DEFAULT_THEME);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored && THEMES.includes(stored)) {
      setThemeState(stored);
    }
    setMounted(true);
  }, []);

  const setTheme = useCallback((newTheme) => {
    if (THEMES.includes(newTheme)) {
      setThemeState(newTheme);
      localStorage.setItem(STORAGE_KEY, newTheme);
    }
  }, []);

  useEffect(() => {
    if (mounted) {
      document.documentElement.setAttribute("data-theme", theme);
    }
  }, [theme, mounted]);

  // Prevent flash of wrong theme
  if (!mounted) {
    return (
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              var t = localStorage.getItem("${STORAGE_KEY}") || "${DEFAULT_THEME}";
              document.documentElement.setAttribute("data-theme", t);
            })();
          `,
        }}
      />
    );
  }

  return (
    <ThemeContext.Provider value={{ theme, setTheme, themes: THEMES }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}
