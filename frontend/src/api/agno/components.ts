import agnoRequest from "./agnoRequest";

export interface AgnoComponent {
  component_id: string;
  component_type?: string;
  name?: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
  [key: string]: any;
}

export interface ComponentConfig {
  version: number;
  config?: Record<string, any>;
  is_current?: boolean;
  created_at?: string;
  updated_at?: string;
  [key: string]: any;
}

const AgnoComponentsAPI = {
  listComponents(params?: { component_type?: string }) {
    return agnoRequest<AgnoComponent[]>({
      url: "/components",
      method: "get",
      params,
    });
  },

  getComponent(componentId: string) {
    return agnoRequest<AgnoComponent>({
      url: `/components/${componentId}`,
      method: "get",
    });
  },

  getConfigs(componentId: string) {
    return agnoRequest<ComponentConfig[]>({
      url: `/components/${componentId}/configs`,
      method: "get",
    });
  },

  getCurrentConfig(componentId: string) {
    return agnoRequest<ComponentConfig>({
      url: `/components/${componentId}/configs/current`,
      method: "get",
    });
  },

  getConfigByVersion(componentId: string, version: number) {
    return agnoRequest<ComponentConfig>({
      url: `/components/${componentId}/configs/${version}`,
      method: "get",
    });
  },
};

export default AgnoComponentsAPI;
