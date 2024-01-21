import React from "react";

import { getApolloClient } from "~/apollo/client";
import { Block, queryPagePreview } from "~/types";

export const usePagePreview = () => {
  const [previewState, setPreviewState] = React.useState({
    contentType: "",
    token: "",
  });
  const [previewBlocks, setPreviewBlocks] = React.useState<Block[] | null>(
    null,
  );

  React.useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setPreviewState({
      contentType: params.get("content_type") || "",
      token: params.get("token") || "",
    });
  }, []);

  React.useEffect(() => {
    if (!previewState.token) {
      return;
    }

    const fetchData = async () => {
      const apolloClient = getApolloClient();
      const response = await queryPagePreview(apolloClient, {
        contentType: previewState.contentType,
        token: previewState.token,
      });
      setPreviewBlocks(response.data.pagePreview.body as any);
    };

    fetchData();
  }, [previewState]);

  return { isPreview: previewState.token !== "", previewBlocks };
};
