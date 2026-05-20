import agnoRequest from "./agnoRequest";

export interface TraceSummary {
  trace_id: string;
  name?: string;
  status?: string;
  duration?: string;
  start_time?: string;
  total_spans?: number;
  error_count?: number;
  input?: string;
  run_id?: string;
  session_id?: string;
  user_id?: string;
  agent_id?: string;
  team_id?: string;
  workflow_id?: string;
  created_at?: string;
}

export interface TraceNode {
  id: string;
  name?: string;
  type?: string;
  duration?: string;
  status?: string;
  input?: string;
  output?: string;
  error?: string;
  metadata?: Record<string, any>;
  spans?: TraceNode[];
}

export interface TraceDetail extends TraceSummary {
  end_time?: string;
  output?: string;
  error?: string;
  tree?: TraceNode[];
}

export interface PaginatedResponse<T> {
  data: T[];
  meta?: {
    page?: number;
    limit?: number;
    total_pages?: number;
    total_count?: number;
    search_time_ms?: number;
  };
}

export interface TraceSessionStats {
  session_id: string;
  user_id?: string;
  agent_id?: string;
  team_id?: string;
  workflow_id?: string;
  total_traces?: number;
  first_trace_at?: string;
  last_trace_at?: string;
}

const AgnoTracesAPI = {
  listTraces(params?: {
    run_id?: string;
    session_id?: string;
    user_id?: string;
    agent_id?: string;
    status?: string;
    page?: number;
    limit?: number;
  }) {
    return agnoRequest<PaginatedResponse<TraceSummary>>({
      url: "/traces",
      method: "get",
      params,
    });
  },

  getTrace(traceId: string, params?: { span_id?: string; run_id?: string }) {
    return agnoRequest<TraceDetail>({
      url: `/traces/${traceId}`,
      method: "get",
      params,
    });
  },

  getTraceSessionStats(params?: {
    user_id?: string;
    agent_id?: string;
    page?: number;
    limit?: number;
  }) {
    return agnoRequest<PaginatedResponse<TraceSessionStats>>({
      url: "/trace_session_stats",
      method: "get",
      params,
    });
  },
};

export default AgnoTracesAPI;
