import agnoRequest from "./agnoRequest";

const AgnoMetricsAPI = {
  getMetrics(params?: { db_id?: string }) {
    return agnoRequest<any>({
      url: "/metrics",
      method: "get",
      params,
    });
  },

  refreshMetrics(params?: { db_id?: string }) {
    return agnoRequest<any>({
      url: "/metrics/refresh",
      method: "post",
      params,
    });
  },
};

export default AgnoMetricsAPI;
