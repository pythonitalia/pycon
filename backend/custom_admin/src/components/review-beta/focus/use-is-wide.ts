import { useEffect, useState } from "react";

const WIDE_QUERY = "(min-width: 1024px)";

export const useIsWide = () => {
  const [isWide, setIsWide] = useState(
    () => window.matchMedia(WIDE_QUERY).matches,
  );

  useEffect(() => {
    const query = window.matchMedia(WIDE_QUERY);
    const onChange = () => setIsWide(query.matches);
    query.addEventListener("change", onChange);
    return () => query.removeEventListener("change", onChange);
  }, []);

  return isWide;
};
