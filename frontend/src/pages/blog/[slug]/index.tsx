import {
  Container,
  Heading,
  Page,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { parseISO } from "date-fns";
import { FormattedMessage } from "react-intl";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Article } from "~/components/article";
import { MetaTags } from "~/components/meta-tags";
import { compile } from "~/helpers/markdown";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryBlogIndex, queryPost, usePostQuery } from "~/types";

export const BlogArticlePage = () => {
  const language = useCurrentLanguage();
  const router = useRouter();
  const slug = router.query.slug as string;
  const dateFormatter = new Intl.DateTimeFormat(language, {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  const { data } = usePostQuery({
    variables: {
      language,
      slug,
    },
  });

  const post = data.blogPost;

  return (
    <Page endSeparator={false}>
      <MetaTags
        title={post.title}
        description={post.excerpt || post.title}
        useDefaultSocialCard={false}
        useNewSocialCard={true}
      />

      <Section illustration="snakeHead">
        <Text size={2}>
          <FormattedMessage
            id="blog.publishedOn"
            values={{
              date: dateFormatter.format(parseISO(post.published)),
              author: post.author.fullName,
            }}
          />
        </Text>
        <Spacer size="medium" />
        <Heading size={1}>{post.title}</Heading>
      </Section>

      <Section illustration="snakeTail">
        <Container noPadding center={false} size="medium">
          <Article>{compile(post.content).tree}</Article>
        </Container>
      </Section>
    </Page>
  );
};

export const getStaticProps: GetStaticProps = async ({ params, locale }) => {
  const slug = params.slug as string;
  const client = getApolloClient();

  const [_, post] = await Promise.all([
    prefetchSharedQueries(client, locale),
    queryPost(client, {
      slug,
      language: locale,
    }),
  ]);

  if (!post.data || !post.data.blogPost) {
    return {
      notFound: true,
    };
  }

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () => {
  const client = getApolloClient();

  const [
    {
      data: { blogPosts: italianBlogPosts },
    },
    {
      data: { blogPosts: englishBlogPosts },
    },
  ] = await Promise.all([
    queryBlogIndex(client, {
      language: "it",
    }),
    queryBlogIndex(client, {
      language: "en",
    }),
  ]);

  const paths = [
    ...italianBlogPosts.map((blogPost) => ({
      params: {
        slug: blogPost.slug,
      },
      locale: "it",
    })),
    ...englishBlogPosts.map((blogPost) => ({
      params: {
        slug: blogPost.slug,
      },
      locale: "en",
    })),
  ];

  return {
    paths,
    fallback: "blocking",
  };
};

export default BlogArticlePage;
