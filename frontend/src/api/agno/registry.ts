import agnoRequest from "./agnoRequest";

const AgnoRegistryAPI = {
  getRegistry() {
    return agnoRequest<any>({
      url: "/registry",
      method: "get",
    });
  },
};

export default AgnoRegistryAPI;
