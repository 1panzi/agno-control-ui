import agnoRequest from "./agnoRequest";

export interface Memory {
  id: string;
  memory?: string;
  topic?: string;
  user_id?: string;
  created_at?: string;
  updated_at?: string;
  [key: string]: any;
}

export interface MemoryTopic {
  topic: string;
  count: number;
}

export interface UserMemoryStats {
  user_id: string;
  total_memories: number;
  topics: string[];
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

const AgnoMemoriesAPI = {
  listMemories(params?: {
    user_id?: string;
    topic?: string;
    page?: number;
    limit?: number;
  }) {
    return agnoRequest<PaginatedResponse<Memory>>({
      url: "/memories",
      method: "get",
      params,
    });
  },

  getMemory(memoryId: string) {
    return agnoRequest<Memory>({
      url: `/memories/${memoryId}`,
      method: "get",
    });
  },

  deleteMemory(memoryId: string) {
    return agnoRequest({
      url: `/memories/${memoryId}`,
      method: "delete",
    });
  },

  deleteAllMemories(params?: { user_id?: string }) {
    return agnoRequest({
      url: "/memories",
      method: "delete",
      params,
    });
  },

  getTopics(params?: { user_id?: string }) {
    return agnoRequest<MemoryTopic[]>({
      url: "/memory_topics",
      method: "get",
      params,
    });
  },

  getUserStats(params?: { user_id?: string; page?: number; limit?: number }) {
    return agnoRequest<PaginatedResponse<UserMemoryStats>>({
      url: "/user_memory_stats",
      method: "get",
      params,
    });
  },
};

export default AgnoMemoriesAPI;
