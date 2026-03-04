import { create } from 'zustand';

type AppState = {
  safeMode: boolean;
  setSafeMode: (value: boolean) => void;
};

export const useAppStore = create<AppState>((set) => ({
  safeMode: false,
  setSafeMode: (safeMode) => set({ safeMode }),
}));
