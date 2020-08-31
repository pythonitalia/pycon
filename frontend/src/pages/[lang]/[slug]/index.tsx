/** @jsx jsx */
import { useRouter } from "next/router";
import { Fragment } from "react";
import { Box, jsx } from "theme-ui";

import { Article } from "~/components/article";
import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { compile } from "~/helpers/markdown";
import { useCurrentLanguage } from "~/locale/context";
import ErrorPage from "~/pages/_error";
import { usePageQuery } from "~/types";

export const Page = () => {
  const router = useRouter();
  const slug = router.query.slug as string;
  const language = useCurrentLanguage();

  const { data, loading } = usePageQuery({
    variables: {
      code: process.env.conferenceCode,
      language,
      slug,
    },
  });

  if (loading) {
    return <PageLoading titleId="global.loading" />;
  }

  if (!data) {
    return <ErrorPage statusCode={404} />;
  }

  const { page } = data;

  if (!page) {
    return <ErrorPage statusCode={404} />;
  }

  return (
    <Fragment>
      <MetaTags title={page.title} />

      <Box sx={{ mx: "auto", px: 3, py: 5, maxWidth: "container" }}>
        <Article title={page.title}>{compile(page.content).tree}</Article>
      </Box>
    </Fragment>
  );
};

export default Page;
