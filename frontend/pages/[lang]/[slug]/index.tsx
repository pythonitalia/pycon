/** @jsx jsx */
import { Box, Text } from "@theme-ui/components";
import { useRouter } from "next/router";
import { Fragment } from "react";
import { jsx } from "theme-ui";

import { Article } from "~/components/article";
import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { compile } from "~/helpers/markdown";
import { useCurrentLanguage } from "~/locale/context";
import { usePageQuery } from "~/types";

export default () => {
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
    return <PageLoading />;
  }

  if (!data) {
    return null;
  }

  const { page } = data;

  return (
    <Fragment>
      <MetaTags title={page.title} />

      <Box sx={{ mx: "auto", px: 3, py: 5, maxWidth: "container" }}>
        <Article title={page.title}>{compile(page.content).tree}</Article>
      </Box>
    </Fragment>
  );
};
