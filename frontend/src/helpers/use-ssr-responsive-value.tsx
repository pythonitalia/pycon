import { useResponsiveValue } from "@theme-ui/match-media";

export const useSSRResponsiveValue = (values: any[]) => {
  if (typeof window === "undefined") {
    return values[0];
  }

  // eslint-disable-next-line react-hooks/rules-of-hooks
  return useResponsiveValue(values);
};
