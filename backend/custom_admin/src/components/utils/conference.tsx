export const useCurrentConference = (): {
  conferenceCode: string;
  conferenceId: string;
} => {
  return {
    conferenceId: (window as any).conferenceId,
    conferenceCode: (window as any).conferenceCode,
  };
};
