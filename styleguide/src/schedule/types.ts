export type Performer = {
  fullName: string;
  profilePicture: string | null;
  bio?: string | null;
  twitter?: string | null;
  website?: string | null;
};

export type Status = "CONFIRMED" | "TBC" | "CANCELLED";

export type BaseEvent = {
  start: string;
  actualStart?: string;
  end: string;
  title?: string;
  slug?: string;
  status: Status;
  size?: number;
  type:
    | "LIVE_CODING"
    | "PERFORMANCE"
    | "INTERMISSION"
    | "INTERVIEW"
    | "LIGHTNING_TALK"
    | "QUIZ"
    | "CLOSING"
    | "DIVERSITY_SUCCESS_STORY"
    | "AMA";
};

export type EventWithPerformer = BaseEvent & {
  performer: Performer | null;
};

export type EventWithPerformers = BaseEvent & {
  performers: Performer[];
};

export type Event = BaseEvent | EventWithPerformer | EventWithPerformers;

export type ScheduleDay = {
  date: string;
  mc: Performer & {
    status: Status;
  };
  events: Event[];
};

export type ScheduleProgram = {
  days: ScheduleDay[];
};
