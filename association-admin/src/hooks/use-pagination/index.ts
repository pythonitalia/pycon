import { useCallback, useState } from "react";

const ITEMS_COUNT = 10;

export const usePagination = () => {
  const [after, setAfter] = useState(0);
  const [to, setTo] = useState(ITEMS_COUNT);

  const goNext = useCallback(() => {
    setAfter(to);
    setTo(to + ITEMS_COUNT);
  }, [to]);

  const goBack = useCallback(() => {
    setAfter(after - ITEMS_COUNT);
    setTo(after);
  }, [after]);

  return {
    to,
    after,
    goNext,
    goBack,
  };
};
