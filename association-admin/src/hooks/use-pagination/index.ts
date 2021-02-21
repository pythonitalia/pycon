import { useCallback } from "react";

import { useRouter } from "next/router";

import { clamp } from "~/helpers/clamp";

const ITEMS_COUNT = 10;

export const usePagination = (urlPrefix) => {
  const { replace, pathname } = useRouter();

  const queryAfter = `${urlPrefix}-after`;
  const queryTo = `${urlPrefix}-to`;

  let after: number | null = null;
  let to: number | null = null;

  if (typeof window !== "undefined") {
    const searchParams = new window.URLSearchParams(window.location.search);
    after = parseInt(searchParams.get(queryAfter), 10) || 0;
    to = parseInt(searchParams.get(queryTo), 10) || ITEMS_COUNT;
  }

  const replaceUrl = (newAfter: number, newTo: number) => {
    replace(
      {
        pathname,
        query: {
          [queryAfter]: Math.max(0, newAfter),
          [queryTo]: Math.max(1, newTo),
        },
      },
      null,
      { shallow: true },
    );
  };

  const goNext = useCallback(() => {
    replaceUrl(to, to + ITEMS_COUNT);
  }, [to]);

  const goBack = useCallback(() => {
    replaceUrl(after - ITEMS_COUNT, after);
  }, [after]);

  return {
    to,
    after,
    goNext,
    goBack,
  };
};
