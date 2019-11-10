import { useResponsiveValue } from "@theme-ui/match-media";

export const useSSRResponsiveValue = (values: any[]) => {
  if (typeof window === "undefined") {
    return values[0];
  }

  return useResponsiveValue(values);
};
