/** @jsxImportSource theme-ui */
import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";
import { Fragment } from "react";
import { Box, jsx } from "theme-ui";

import { addApolloState } from "~/apollo/client";
import { Article } from "~/components/article";
import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { compile } from "~/helpers/markdown";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import Error404 from "~/pages/404";
import { queryAllPages, queryPage, usePageQuery } from "~/types";

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
    return <Error404 />;
  }

  const { page } = data;

  if (!page) {
    return <Error404 />;
  }

  return (
    <Fragment>
      <MetaTags title={page.title} />

      <Box sx={{ mx: "auto", px: 3, maxWidth: "container" }}>
        <Article title={page.title}>{compile(page.content).tree}</Article>
      </Box>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const language = params.lang as string;
  const slug = params.slug as string;

  await prefetchSharedQueries(language);

  await queryPage({
    code: process.env.conferenceCode,
    language,
    slug,
  });

  return addApolloState({
    props: {},
    revalidate: 1,
  });
};

export const getStaticPaths: GetStaticPaths = async () => {
  const {
    data: { pages: italianPages },
  } = await queryAllPages({
    code: process.env.conferenceCode,
    language: "it",
  });
  const {
    data: { pages: englishPages },
  } = await queryAllPages({
    code: process.env.conferenceCode,
    language: "en",
  });

  const paths = [
    ...italianPages.map((page) => ({
      params: {
        lang: "it",
        slug: page.slug,
      },
    })),
    ...englishPages.map((page) => ({
      params: {
        lang: "en",
        slug: page.slug,
      },
    })),
  ];

  return {
    paths,
    fallback: false,
  };
};

export default Page;
