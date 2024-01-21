import { PageHandler } from "~/components/page-handler";

export { getStaticProps } from "~/components/page-handler/page-static-props";

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
