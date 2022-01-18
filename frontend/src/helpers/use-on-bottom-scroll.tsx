import { useEffect, useCallback } from "react";

export const useOnBottomScroll = (callback: () => void) => {
  const listener = useCallback(() => {
    const scrollNode = document.scrollingElement || document.documentElement;
    const scrollContainerBottomPosition = Math.round(
      scrollNode.scrollTop + window.innerHeight,
    );
    const scrollPosition = Math.round(scrollNode.scrollHeight - 0);

    if (scrollPosition <= scrollContainerBottomPosition) {
      callback();
    }
  }, [callback]);

  useEffect(() => {
    window.addEventListener("scroll", listener);
    return () => {
      window.removeEventListener("scroll", listener);
    };
  }, [listener]);
};
