import agnoRequest from "./agnoRequest";

export interface Schedule {
  schedule_id: string;
  name?: string;
  description?: string;
  cron_expression?: string;
  enabled?: boolean;
  agent_id?: string;
  team_id?: string;
  workflow_id?: string;
  created_at?: string;
  updated_at?: string;
  last_run_at?: string;
  next_run_at?: string;
  [key: string]: any;
}

export interface ScheduleRun {
  run_id: string;
  schedule_id?: string;
  status?: string;
  started_at?: string;
  completed_at?: string;
  [key: string]: any;
}

const AgnoSchedulesAPI = {
  listSchedules() {
    return agnoRequest<Schedule[]>({
      url: "/schedules",
      method: "get",
    });
  },

  getSchedule(scheduleId: string) {
    return agnoRequest<Schedule>({
      url: `/schedules/${scheduleId}`,
      method: "get",
    });
  },

  enableSchedule(scheduleId: string) {
    return agnoRequest({
      url: `/schedules/${scheduleId}/enable`,
      method: "post",
    });
  },

  disableSchedule(scheduleId: string) {
    return agnoRequest({
      url: `/schedules/${scheduleId}/disable`,
      method: "post",
    });
  },

  triggerSchedule(scheduleId: string) {
    return agnoRequest({
      url: `/schedules/${scheduleId}/trigger`,
      method: "post",
    });
  },

  getScheduleRuns(scheduleId: string) {
    return agnoRequest<ScheduleRun[]>({
      url: `/schedules/${scheduleId}/runs`,
      method: "get",
    });
  },

  getScheduleRun(scheduleId: string, runId: string) {
    return agnoRequest<ScheduleRun>({
      url: `/schedules/${scheduleId}/runs/${runId}`,
      method: "get",
    });
  },
};

export default AgnoSchedulesAPI;
