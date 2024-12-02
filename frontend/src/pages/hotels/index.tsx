import type { GetServerSideProps } from "next";
import { useRouter } from "next/router";
import { PageHandler } from "~/components/page-handler";
import { getProps } from "~/components/page-handler/page-static-props";

export const HotelsPage = ({ blocksProps, isPreview, previewData }) => {
  const router = useRouter();
  const slug = router.query.slug as string;
  return (
    <PageHandler
      isPreview={isPreview}
      previewData={previewData}
      slug={slug}
      blocksProps={blocksProps}
    />
  );
};

export const getServerSideProps: GetServerSideProps = async (context: any) => {
  return getProps(context);
};
