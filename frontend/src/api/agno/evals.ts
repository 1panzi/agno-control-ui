import agnoRequest from "./agnoRequest";

export interface EvalRun {
  eval_run_id: string;
  name?: string;
  status?: string;
  agent_id?: string;
  team_id?: string;
  workflow_id?: string;
  total_tests?: number;
  passed_tests?: number;
  failed_tests?: number;
  created_at?: string;
  updated_at?: string;
  [key: string]: any;
}

export interface PaginatedResponse<T> {
  data: T[];
  meta?: {
    page?: number;
    limit?: number;
    total_pages?: number;
    total_count?: number;
  };
}

const AgnoEvalsAPI = {
  listEvalRuns(params?: {
    agent_id?: string;
    status?: string;
    page?: number;
    limit?: number;
  }) {
    return agnoRequest<PaginatedResponse<EvalRun>>({
      url: "/eval-runs",
      method: "get",
      params,
    });
  },

  getEvalRun(evalRunId: string) {
    return agnoRequest<EvalRun>({
      url: `/eval-runs/${evalRunId}`,
      method: "get",
    });
  },
};

export default AgnoEvalsAPI;
