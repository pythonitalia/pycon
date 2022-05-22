export const ItemTypes = {
  ALL_TRACKS_EVENT: "all_tracks_event",
  TRAINING: "training",
  TALK: "talk",
  CUSTOM: "custom",
  KEYNOTE: "keynote",
  ROOM_CHANGE: "room_change",
};

export type Submission = {
  id: string;
  title: string;
  type?: { name: string } | null;
  duration?: { duration: number } | null;
  audienceLevel?: { name: string } | null;
  speaker?: { fullName: string } | null;
};

type KeynoteSpeaker = {
  id: string;
  name: string;
  photo: string;
  highlightColor: string;
};

export type Keynote = {
  id: string;
  title: string;
  slug: string;
  speakers: KeynoteSpeaker[];
};

export type Item = {
  id: string;
  title: string;
  slug: string;
  language: { code: string };
  type: string;
  rooms: Room[];
  duration?: number | null;
  submission?: Submission | null;
  keynote?: Keynote | null;
  audienceLevel?: { name: string } | null;
  speakers: { fullName: string }[];
  hasLimitedCapacity: boolean;
  userHasSpot: boolean;
  hasSpacesLeft: boolean;
  spacesLeft: number;
};

export type Slot = {
  id: string;
  duration: number;
  hour: string;
  type: "DEFAULT" | "FREE_TIME";
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
