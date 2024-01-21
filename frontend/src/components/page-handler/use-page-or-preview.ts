import { useCurrentLanguage } from "~/locale/context";
import { usePagePreviewQuery, usePageQuery } from "~/types";

export const usePageOrPreview = ({
  slug,
  isPreview,
  previewData,
}: {
  slug: string;
  isPreview: boolean;
  previewData: any;
}) => {
  const language = useCurrentLanguage();

  const { data: pageReqData } = usePageQuery({
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
  return isPreview ? previewReqData.pagePreview : pageReqData.cmsPage;
};
