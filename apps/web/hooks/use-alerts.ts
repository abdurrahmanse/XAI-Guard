import { useQuery } from "@tanstack/react-query";
import { ApiClient } from "../lib/api-client";

export function useAlerts() {
  return useQuery({
    queryKey: ["alerts"],
    queryFn: () => ApiClient.get("/alerts"),
    refetchInterval: 5000, // Poll every 5s as fallback to websockets
  });
}
