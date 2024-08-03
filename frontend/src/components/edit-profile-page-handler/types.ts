import type { ParticipantFormFields } from "../public-profile-card";

export type MeUserFields = ParticipantFormFields & {
  name: string;
  fullName: string;
  gender: string;
  dateBirth: Date;
  country: string;
  openToRecruiting: boolean;
  openToNewsletter: boolean;

  participantSpeakerLevel: string;
  participantPreviousTalkVideo: string;
};
