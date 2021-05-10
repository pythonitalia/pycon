export type Performer = {
  fullName: string;
  profilePicture: string;
};

export type Status = "CONFIRMED" | "TBC";

export type BaseEvent = {
  start: string;
  end: string;
  title: string;
  type:
    | "LIVE_CODING"
    | "PERFORMANCE"
    | "INTERMISSION"
    | "LIGHTNING_TALK"
    | "QUIZ"
    | "CLOSING"
    | "ARTISTIC_PERFORMANCE"
    | "DIVERSITY_SUCCESS_STORY"
    | "AMA";
};

export type EventWithPerformer = BaseEvent & {
  status: Status;
  performer: Performer;
};

export type EventWithPerformers = BaseEvent & {
  status: Status;
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
