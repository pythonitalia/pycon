import type { GetServerSideProps } from "next";
import { useRouter } from "next/router";
import { PageHandler } from "~/components/page-handler";
import { getProps } from "~/components/page-handler/page-static-props";

export const HotelsPage = ({ blocksProps, isPreview, previewData }) => {
  const router = useRouter();
  return (
    <PageHandler
      isPreview={isPreview}
      previewData={previewData}
      slug="hotels"
      blocksProps={blocksProps}
    />
  );
};

export const getServerSideProps: GetServerSideProps = async (context: any) => {
  return getProps({
    ...context,
    params: {
      slug: "hotels",
    },
    revalidate: null,
  });
};

export default HotelsPage;
