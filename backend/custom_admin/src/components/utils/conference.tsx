export const useCurrentConference = (): string => {
  return (window as any).conferenceId;
};
