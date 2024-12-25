import { useArgs } from "../shared/args";

export const useCurrentConference = (): {
  conferenceCode: string;
  conferenceId: string;
} => {
  const { conferenceId, conferenceCode } = useArgs();
  return {
    conferenceId,
    conferenceCode,
  };
};
