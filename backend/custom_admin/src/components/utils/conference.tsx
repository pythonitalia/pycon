import { getArg } from "../shared/get-arg";

export const useCurrentConference = (): {
  conferenceCode: string;
  conferenceId: string;
} => {
  return {
    conferenceId: getArg("conference_id"),
    conferenceCode: getArg("conference_code"),
  };
};
