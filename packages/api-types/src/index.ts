import { z } from "zod";

export const SecurityEventInputSchema = z.object({
  source_ip: z.string().ip(),
  destination_ip: z.string().ip(),
  source_port: z.number().int().min(0).max(65535),
  destination_port: z.number().int().min(0).max(65535),
  protocol: z.enum(["TCP", "UDP", "ICMP", "OTHER"]),
  timestamp: z.string().datetime(),
  duration_ms: z.number().min(0),
  bytes_sent: z.number().int().min(0),
  bytes_received: z.number().int().min(0),
  packet_count: z.number().int().min(0),
  tcp_flags: z.record(z.boolean()),
  service: z.string().max(64),
  features: z.record(z.number()),
  dataset_source: z.enum(["NSL_KDD", "CICIDS_2017", "UNSW_NB15", "BETH", "LIVE"]),
});

export const PredictionResponseSchema = z.object({
  id: z.string().uuid(),
  event_id: z.string().uuid(),
  predicted_class: z.string(),
  confidence_score: z.number().min(0).max(1),
  class_probabilities: z.record(z.number()),
  severity_level: z.enum(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
  inference_latency_ms: z.number(),
  is_shadow: z.boolean(),
  explanation_task_id: z.string().nullable().optional(),
  created_at: z.string().datetime(),
});

export class ApiValidationError extends Error {
  constructor(public zodError: z.ZodError) {
    super("API Response Validation Failed");
    this.name = "ApiValidationError";
  }
}

export function validateApiResponse<T>(schema: z.ZodSchema<T>, data: unknown): T {
  const result = schema.safeParse(data);
  if (!result.success) {
    throw new ApiValidationError(result.error);
  }
  return result.data;
}

export async function zodFetcher<T>(url: string, schema: z.ZodSchema<T>, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  const data = await response.json();
  return validateApiResponse(schema, data);
}

export type SecurityEventInput = z.infer<typeof SecurityEventInputSchema>;
export type PredictionResponse = z.infer<typeof PredictionResponseSchema>;
