import { createContext, useContext, useMemo } from "react";

const ArgsContext = createContext<Record<string, any>>({});

export const useArgs = () => {
  return useContext(ArgsContext);
};

export const ArgsProvider = ({ children, args }) => {
  const resolvedArgs = useMemo(() => {
    return Object.entries(args).reduce((acc, [key, value]) => {
      try {
        acc[key] = JSON.parse(value as string);
      } catch (e) {
        acc[key] = value;
      }
      return acc;
    }, {});
  }, [args]);

  return (
    <ArgsContext.Provider value={resolvedArgs}>{children}</ArgsContext.Provider>
  );
};
