import React, { useContext } from "react";

export const ConferenceContext = React.createContext<string>("");

export const useConference = () => {
  const code = useContext(ConferenceContext);

  return { code };
};
