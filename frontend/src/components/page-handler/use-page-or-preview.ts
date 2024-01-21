import { useCurrentLanguage } from "~/locale/context";
import {
  useNewsArticleQuery,
  usePagePreviewQuery,
  usePageQuery,
} from "~/types";

const useFetch = (fetcher: "page" | "newsArticle") => {
  let fetcherFunc = null;
  switch (fetcher) {
    case "page":
      fetcherFunc = usePageQuery;
      break;
    case "newsArticle":
      fetcherFunc = useNewsArticleQuery;
      break;
  }

  return fetcherFunc;
};

export const usePageOrPreview = ({
  fetcher,
  slug,
  isPreview,
  previewData,
}: {
  fetcher: "page" | "newsArticle";
  slug: string;
  isPreview: boolean;
  previewData: any;
}) => {
  const language = useCurrentLanguage();

  const { data: pageData } = useFetch(fetcher)({
    variables: {
      hostname: process.env.cmsHostname,
      language,
      slug,
    },
    skip: isPreview,
  });

  const { data: previewReqData } = usePagePreviewQuery({
    variables: {
      contentType: previewData?.contentType,
      token: previewData?.token,
    },
    skip: !isPreview,
  });

  if (isPreview) {
    switch (previewReqData.pagePreview.__typename) {
      case "GenericPagePreview":
        return previewReqData?.pagePreview.genericPage;
      case "NewsArticlePreview":
        return previewReqData?.pagePreview.newsArticle;
    }
  }

  switch (fetcher) {
    case "page":
      return pageData.cmsPage;
    case "newsArticle":
      return pageData.newsArticle;
  }
};
