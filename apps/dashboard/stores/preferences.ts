import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface PreferencesState {
  alertSoundEnabled: boolean;
  compactMode: boolean;
  explanationMethod: "SHAP" | "LIME";
  toggleSound: () => void;
  toggleCompactMode: () => void;
  setExplanationMethod: (method: "SHAP" | "LIME") => void;
}

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    immer((set) => ({
      alertSoundEnabled: true,
      compactMode: false,
      explanationMethod: "SHAP",
      toggleSound: () => set((state) => { state.alertSoundEnabled = !state.alertSoundEnabled; }),
      toggleCompactMode: () => set((state) => { state.compactMode = !state.compactMode; }),
      setExplanationMethod: (method) => set((state) => { state.explanationMethod = method; })
    })),
    {
      name: 'xaiguard-preferences',
    }
  )
);
