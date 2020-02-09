export const ItemTypes = {
  ALL_TRACKS_EVENT: "all_tracks_event",
  TRAINING: "training",
  CUSTOM: "custom",
};

export type Item = {
  id: string;
  title: string;
  rooms: Room[];
};

export type Slot = {
  id: string;
  duration: number;
  hour: string;
  size: number;
  offset: number;
  items: Item[];
};

export type ScheduleItem = {
  title: string;
  trackSpan?: number;
  allTracks?: boolean;
};

export type Room = {
  id: string;
  name: string;
  type: string;
};
