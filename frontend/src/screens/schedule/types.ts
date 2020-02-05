import moment from "moment";

export const ItemTypes = {
  TALK_30: "talk_30",
  TALK_45: "talk_45",
  TALK_60: "talk_60",
  ALL_TRACKS_EVENT: "all_tracks_event",
};

export type Slot = {
  duration: number;
  hour: string;
  size: number;
  offset: number;
};

export type ScheduleItem = {
  title: string;
  trackSpan?: number;
  allTracks?: boolean;
};

export type Room = {
  name: string;
};
