import agnoRequest from "./agnoRequest";

export interface Approval {
  approval_id: string;
  run_id?: string;
  session_id?: string;
  agent_id?: string;
  tool_name?: string;
  tool_args?: Record<string, any>;
  status?: string;
  resolved_at?: string;
  created_at?: string;
  [key: string]: any;
}

const AgnoApprovalsAPI = {
  listApprovals(params?: {
    agent_id?: string;
    status?: string;
    page?: number;
    limit?: number;
  }) {
    return agnoRequest<Approval[]>({
      url: "/approvals",
      method: "get",
      params,
    });
  },

  getApproval(approvalId: string) {
    return agnoRequest<Approval>({
      url: `/approvals/${approvalId}`,
      method: "get",
    });
  },

  getApprovalStatus(approvalId: string) {
    return agnoRequest<any>({
      url: `/approvals/${approvalId}/status`,
      method: "get",
    });
  },

  getApprovalCount(params?: { agent_id?: string; status?: string }) {
    return agnoRequest<any>({
      url: "/approvals/count",
      method: "get",
      params,
    });
  },

  resolveApproval(approvalId: string, data: { approved: boolean; reason?: string }) {
    return agnoRequest({
      url: `/approvals/${approvalId}/resolve`,
      method: "post",
      data,
    });
  },

  deleteApproval(approvalId: string) {
    return agnoRequest({
      url: `/approvals/${approvalId}`,
      method: "delete",
    });
  },
};

export default AgnoApprovalsAPI;
