import agnoRequest from "./agnoRequest";
import { createRunStream } from "./chat";
import type { RunForm, AgentRunResponse, AgentStreamEvent } from "./chat";

const WORKFLOW_PATH = "/workflows";

export interface AgnoWorkflow {
  id: string;
  name?: string;
  description?: string;
}

export const AgnoWorkflowAPI = {
  listWorkflows() {
    return agnoRequest<AgnoWorkflow[]>({
      url: WORKFLOW_PATH,
      method: "get",
    });
  },
};

const AgnoWorkflowChatAPI = {
  runWorkflow(workflowId: string, body: RunForm) {
    const formData = new FormData();
    formData.append("message", body.message);
    formData.append("stream", "false");
    formData.append("session_id", body.session_id);
    formData.append("user_id", String(body.user_id));
    formData.append("background", "false");
    if (body.version !== undefined) formData.append("version", body.version ?? "");
    if (body.files?.length) {
      body.files.forEach((f) => formData.append("files", f));
    }
    return agnoRequest<AgentRunResponse>({
      url: `${WORKFLOW_PATH}/${workflowId}/runs`,
      method: "post",
      data: formData,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  runWorkflowStream(
    workflowId: string,
    body: RunForm,
    onChunk: (event: string, data: AgentStreamEvent) => void,
    onDone: () => void,
    onError: (err: Error) => void
  ): AbortController {
    return createRunStream(`${WORKFLOW_PATH}/${workflowId}/runs`, body, onChunk, onDone, onError);
  },
};

export default AgnoWorkflowChatAPI;
