export const ItemTypes = {
  ALL_TRACKS_EVENT: "all_tracks_event",
  TRAINING: "training",
  TALK: "talk",
  CUSTOM: "custom",
};

export type Submission = {
  id: string;
  title: string;
  type: { name: string } | null;
  duration: { duration: number } | null;
  audienceLevel: { name: string } | null;
  speaker: { fullName: string } | null;
};

export type Item = {
  id: string;
  title: string;
  language: { code: string };
  type: string;
  rooms: Room[];
  duration?: number | null;
  submission?: Submission | null;
  speakers: { fullName: string }[];
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
