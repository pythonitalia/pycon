export const ItemTypes = {
  ALL_TRACKS_EVENT: "all_tracks_event",
  TRAINING: "training",
  CUSTOM: "custom",
};

export type Item = {
  id: string;
  title: string;
  rooms: Room[];
  submission?: {
    type: { name: string } | null;
    duration: { duration: number } | null;
  } | null;
};

export type Slot = {
  id: string;
  duration: number;
  hour: string;
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
