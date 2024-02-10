export const useCurrentConference = (): {
  conferenceCode: string;
  conferenceId: string;
  conferenceRepr: string;
} => {
  return {
    conferenceId: (window as any).conferenceId,
    conferenceCode: (window as any).conferenceCode,
    conferenceRepr: (window as any).conferenceRepr,
  };
};
