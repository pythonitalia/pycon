import { useState, useCallback } from "react";

import { useOnBottomScroll } from "./use-on-bottom-scroll";

export const useInfiniteFetchScroll = ({
  fetchMore,
  hasMoreResultsCallback,
  shouldFetchAgain,
  after,
}: {
  fetchMore: (variables: any) => any;
  hasMoreResultsCallback: (newData: any) => boolean;
  shouldFetchAgain: (newData: any) => any | null;
  after?: number;
}): {
  isFetchingMore: boolean;
  hasMore: boolean;
  forceLoadMore: () => void;
} => {
  const [isFetchingMore, setIsFetchingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const fetchData = async (afterItem: any) => {
    return fetchMore({
      variables: {
        after: afterItem,
        loadMore: true,
      },
    });
  };

  const fetchMoreSubmissionsCallback = useCallback(async () => {
    if (!after || !hasMore || isFetchingMore) {
      return;
    }

    setIsFetchingMore(true);
    let afterItem = after;
    let newData;

    // eslint-disable-next-line
    while (true) {
      const { data: tempData } = await fetchData(afterItem);

      const newAfter = shouldFetchAgain(tempData);

      if (newAfter !== null) {
        afterItem = newAfter;
      } else {
        newData = tempData;
        break;
      }
    }

    setIsFetchingMore(false);

    if (!hasMoreResultsCallback(newData)) {
      setHasMore(false);
    }
  }, [after, hasMore, isFetchingMore]);

  useOnBottomScroll(fetchMoreSubmissionsCallback);

  return {
    isFetchingMore,
    hasMore,
    forceLoadMore: () => {
      fetchMoreSubmissionsCallback();
    },
  };
};
