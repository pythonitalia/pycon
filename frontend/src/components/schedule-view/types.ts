import {
  type ScheduleQuery,
  readUserStarredScheduleItemsQueryCache,
  useStarScheduleItemMutation,
  useUnstarScheduleItemMutation,
  useUserStarredScheduleItemsQuery,
  writeUserStarredScheduleItemsQueryCache,
} from "~/types";

export type Slot = ScheduleQuery["conference"]["days"][0]["slots"][0];
export type Item = Slot["items"][0];
export type Room = ScheduleQuery["conference"]["days"][0]["rooms"][0];
