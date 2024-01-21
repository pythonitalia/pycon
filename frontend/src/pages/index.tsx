import { GetStaticProps } from "next";

import { PageHandler } from "~/components/page-handler";
import { getStaticProps as baseGetStaticProps } from "~/components/page-handler/page-static-props";

export const getStaticProps: GetStaticProps = async (args) => {
  return baseGetStaticProps({
    ...args,
    params: {
      ...args.params,
      slug: process.env.conferenceCode,
    },
  });
};

export default ({ blocksProps, isPreview, previewData }) => {
  return (
    <PageHandler
      isPreview={isPreview}
      previewData={previewData}
      slug={process.env.conferenceCode}
      blocksProps={blocksProps}
    />
  );
};
