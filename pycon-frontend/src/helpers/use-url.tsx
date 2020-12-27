import React from "react";

type URL = {
  host: string;
  path: string;
};

export const URLContext = React.createContext(null);

export const useCurrentUrl = () => React.useContext<URL>(URLContext);
