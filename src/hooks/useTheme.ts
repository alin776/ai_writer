import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

export type ThemePreference = 'light' | 'dark' | 'auto';
type ThemeMode = 'light' | 'dark';

interface ApplyThemeOptions {
  persist?: boolean;
}

const STORAGE_KEY = 'novelaide-theme-preference';
const DARK_MEDIA_QUERY = '(prefers-color-scheme: dark)';

const getSystemTheme = (): ThemeMode => {
  if (typeof window === 'undefined') {
    return 'light';
  }
  return window.matchMedia(DARK_MEDIA_QUERY).matches ? 'dark' : 'light';
};

const applyThemeClass = (theme: ThemeMode) => {
  if (typeof document === 'undefined') return;
  document.documentElement.classList.toggle('dark', theme === 'dark');
};

export function useTheme(initialPreference?: ThemePreference) {
  const resolvedInitial = useMemo<ThemePreference>(() => {
    if (initialPreference) {
      return initialPreference;
    }
    if (typeof window === 'undefined') {
      return 'auto';
    }
    const stored = window.localStorage.getItem(STORAGE_KEY) as ThemePreference | null;
    return stored ?? 'auto';
  }, [initialPreference]);

  const [preference, setPreferenceState] = useState<ThemePreference>(resolvedInitial);
  const [effectiveTheme, setEffectiveTheme] = useState<ThemeMode>(() =>
    resolvedInitial === 'auto' ? getSystemTheme() : resolvedInitial
  );

  const preferenceRef = useRef<ThemePreference>(resolvedInitial);

  const apply = useCallback(
    (nextPreference: ThemePreference, options: ApplyThemeOptions = {}) => {
      const { persist = true } = options;
      preferenceRef.current = nextPreference;
      setPreferenceState(nextPreference);

      const targetTheme = nextPreference === 'auto' ? getSystemTheme() : nextPreference;
      setEffectiveTheme(targetTheme);
      applyThemeClass(targetTheme);

      if (persist && typeof window !== 'undefined') {
        window.localStorage.setItem(STORAGE_KEY, nextPreference);
      }
    },
    []
  );

  useEffect(() => {
    if (typeof window === 'undefined') return;

    apply(resolvedInitial, { persist: false });

    const mediaQuery = window.matchMedia(DARK_MEDIA_QUERY);
    const handleSystemThemeChange = (event: MediaQueryListEvent) => {
      if (preferenceRef.current === 'auto') {
        const nextTheme = event.matches ? 'dark' : 'light';
        setEffectiveTheme(nextTheme);
        applyThemeClass(nextTheme);
      }
    };

    mediaQuery.addEventListener('change', handleSystemThemeChange);

    return () => {
      mediaQuery.removeEventListener('change', handleSystemThemeChange);
    };
  }, [apply, resolvedInitial]);

  return {
    preference,
    effectiveTheme,
    applyTheme: apply,
  };
}
