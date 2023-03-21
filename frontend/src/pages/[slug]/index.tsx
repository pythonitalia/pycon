import { Section, Page as BasePage } from "@python-italia/pycon-styleguide";
import React, { Fragment } from "react";

import { GetStaticPaths, GetStaticProps } from "next";
import Error from "next/error";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Article } from "~/components/article";
import { BlocksRenderer } from "~/components/blocks-renderer";
import { MetaTags } from "~/components/meta-tags";
import { compile } from "~/helpers/markdown";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { GenericPage, queryAllPages, queryPage, usePageQuery } from "~/types";

export const Page = () => {
  const router = useRouter();
  const slug = router.query.slug as string;
  const language = useCurrentLanguage();

  const { data, error } = usePageQuery({
    variables: {
      code: process.env.conferenceCode,
      language,
      slug,
    },
  });

  if (!data) {
    return <Error statusCode={404} />;
  }

  const { page, cmsPage } = data;
  console.log(cmsPage);

  if (!page && (!cmsPage || cmsPage.__typename !== "GenericPage")) {
    return <Error statusCode={404} />;
  }

  return (
    <Fragment>
      <MetaTags title={page.title} />

      <BasePage endSeparator={false}>
        {cmsPage && <BlocksRenderer blocks={(cmsPage as GenericPage).body} />}
        {!cmsPage && (
          <Section>
            <Article title={page.title}>{compile(page.content).tree}</Article>
          </Section>
        )}
      </BasePage>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ params, locale }) => {
  const language = locale;
  const slug = params.slug as string;
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, language),
    queryPage(client, {
      code: process.env.conferenceCode,
      language,
      slug,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () => {
  const client = getApolloClient();

  const {
    data: { pages: italianPages },
  } = await queryAllPages(client, {
    code: process.env.conferenceCode,
    language: "it",
  });
  const {
    data: { pages: englishPages },
  } = await queryAllPages(client, {
    code: process.env.conferenceCode,
    language: "en",
  });

  const paths = [
    ...italianPages.map((page) => ({
      params: {
        slug: page.slug,
      },
      locale: "it",
    })),
    ...englishPages.map((page) => ({
      params: {
        slug: page.slug,
      },
      locale: "en",
    })),
  ];

  return {
    paths,
    fallback: "blocking",
  };
};

export default Page;
