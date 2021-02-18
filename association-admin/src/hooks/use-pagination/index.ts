import { useCallback } from "react";

import { useRouter } from "next/router";

const ITEMS_COUNT = 10;

export const usePagination = (urlPrefix) => {
  const { replace, pathname } = useRouter();

  const queryAfter = `${urlPrefix}-after`;
  const queryTo = `${urlPrefix}-to`;

  let after: number | null = null;
  let to: number | null = null;

  if (typeof window !== "undefined") {
    const searchParams = new window.URLSearchParams(window.location.search);
    after = parseInt(searchParams.get(queryAfter), 10);
    to = parseInt(searchParams.get(queryTo), 10);
  }

  const goNext = useCallback(() => {
    replace(
      {
        pathname,
        query: {
          [queryAfter]: to,
          [queryTo]: to + ITEMS_COUNT,
        },
      },
      null,
      { shallow: true },
    );
  }, [to]);

  const goBack = useCallback(() => {
    replace(
      {
        pathname,
        query: {
          [queryAfter]: after - ITEMS_COUNT,
          [queryTo]: after,
        },
      },
      null,
      { shallow: true },
    );
  }, [after]);

  return {
    to,
    after,
    goNext,
    goBack,
  };
};
