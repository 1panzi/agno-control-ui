import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    basicInfo: { id: 1 } as { id: number },
  }),
});

export function useUserStoreHook() {
  return useUserStore();
}
