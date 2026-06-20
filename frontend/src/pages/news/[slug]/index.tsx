import {
  Container,
  Heading,
  Page,
  Section,
  Spacer,
  StyledHTMLText,
  Text,
} from "@python-italia/pycon-styleguide";
import { parseISO } from "date-fns";
import { FormattedMessage } from "react-intl";

import type { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { MetaTags } from "~/components/meta-tags";
import { usePageOrPreview } from "~/components/page-handler/use-page-or-preview";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { DEFAULT_LOCALE } from "~/locale/languages";
import {
  type NewsArticleQuery,
  type PagePreviewQuery,
  queryAllNewsArticles,
  queryNewsArticle,
  queryPagePreview,
} from "~/types";

export const NewsArticlePage = ({
  isPreview,
  previewData,
}: {
  isPreview: boolean;
  previewData: any;
}) => {
  const language = useCurrentLanguage();
  const router = useRouter();
  const slug = router.query.slug as string;
  const dateFormatter = new Intl.DateTimeFormat(language, {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  const post = usePageOrPreview({
    fetcher: "newsArticle",
    slug,
    isPreview,
    previewData,
  });

  return (
    <Page endSeparator={false}>
      <MetaTags
        title={post.title}
        description={post.excerpt || post.title}
        useDefaultSocialCard={false}
      />

      <Section illustration="snakeHead">
        <Text size={2}>
          <FormattedMessage
            id="blog.publishedOn"
            values={{
              date: post.publishedAt
                ? dateFormatter.format(parseISO(post.publishedAt))
                : "",
              author: post.authorFullname,
            }}
          />
        </Text>
        <Spacer size="medium" />
        <Heading size={1}>{post.title}</Heading>
      </Section>

      <Section illustration="snakeTail">
        <Container noPadding center={false} size="medium">
          <StyledHTMLText text={post.body} baseTextSize={2} />
        </Container>
      </Section>
    </Page>
  );
};

export const getStaticProps: GetStaticProps = async ({
  params,
  preview,
  previewData,
}: {
  params: { slug: string };
  preview: boolean;
  previewData: any;
}) => {
  const slug = params.slug as string;
  const client = getApolloClient();

  const [_, newsArticleQuery] = await Promise.all([
    prefetchSharedQueries(client, DEFAULT_LOCALE),
    preview
      ? queryPagePreview(client, {
          contentType: previewData?.contentType,
          token: previewData?.token,
        })
      : queryNewsArticle(client, {
          slug,
          hostname: process.env.cmsHostname,
          language: DEFAULT_LOCALE,
        }),
  ]);

  const newsArticle = preview
    ? (newsArticleQuery.data as PagePreviewQuery).pagePreview
    : (newsArticleQuery.data as NewsArticleQuery).newsArticle;
  if (!newsArticle) {
    return {
      notFound: true,
    };
  }

  return addApolloState(client, {
    props: {
      isPreview: preview || false,
      previewData: previewData || null,
    },
  });
};

export const getStaticPaths: GetStaticPaths = async () => {
  const client = getApolloClient();

  const {
    data: { newsArticles },
  } = await queryAllNewsArticles(client, {
    language: DEFAULT_LOCALE,
    hostname: process.env.cmsHostname,
  });

  const paths = newsArticles.map((blogPost) => ({
    params: {
      slug: blogPost.slug,
    },
  }));

  return {
    paths,
    fallback: "blocking",
  };
};

export default NewsArticlePage;
