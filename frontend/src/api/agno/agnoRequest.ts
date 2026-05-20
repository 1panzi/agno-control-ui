import axios, {
  type AxiosResponse,
  type AxiosError,
} from "axios";
import qs from "qs";

const agnoRequest = axios.create({
  baseURL: "",
  timeout: 30000,
  headers: { "Content-Type": "application/json;charset=utf-8" },
  paramsSerializer: (params) => qs.stringify(params, { indices: false }),
});

agnoRequest.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    const status = error.response?.status;
    const detail = (error.response?.data as any)?.detail;
    const msg = detail
      ? typeof detail === "string" ? detail : JSON.stringify(detail)
      : `请求失败 (${status ?? "网络错误"})`;
    ElMessage.error(msg);
    return Promise.reject(error);
  }
);

export default agnoRequest;
