import type { GetServerSideProps } from "next";
import { getApolloClient } from "~/apollo/client";
import { PageHandler } from "~/components/page-handler";
import { getProps } from "~/components/page-handler/page-static-props";

export const StreamingPage = ({ blocksProps, isPreview, previewData }) => {
  return (
    <PageHandler
      isPreview={isPreview}
      previewData={previewData}
      slug="streaming"
      blocksProps={blocksProps}
    />
  );
};

export const getServerSideProps: GetServerSideProps = async (context: any) => {
  const { req } = context;
  const client = getApolloClient(null, req.cookies);
  return getProps(
    {
      ...context,
      params: {
        slug: "streaming",
      },
    },
    client,
    null,
  );
};

export default StreamingPage;
