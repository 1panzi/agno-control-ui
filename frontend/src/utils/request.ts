import axios, {
  type AxiosResponse,
  type AxiosInstance,
  type AxiosError,
} from "axios";
import qs from "qs";

const httpRequest: AxiosInstance = axios.create({
  baseURL: "/api/v1/agno_manage",
  timeout: 30000,
  headers: { "Content-Type": "application/json;charset=utf-8" },
  paramsSerializer: (params) => qs.stringify(params, { indices: false }),
});

httpRequest.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const data = response.data;
    if (data.code !== 0) {
      ElMessage.error(data.msg || "请求失败");
      return Promise.reject(new Error(data.msg || "请求失败"));
    }
    if (response.config.method?.toUpperCase() !== "GET") {
      ElMessage.success(data.msg || "操作成功");
    }
    return response;
  },
  (error: AxiosError<ApiResponse>) => {
    if (!error.response) {
      ElMessage.error("网络连接异常");
      return Promise.reject(error);
    }
    const msg = error.response.data?.msg || `请求失败 (${error.response.status})`;
    ElMessage.error(msg);
    return Promise.reject(error);
  }
);

export default httpRequest;
