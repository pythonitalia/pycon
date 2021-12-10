/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx, Text } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Link } from "~/components/link";
import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryBlogIndex, useBlogIndexQuery } from "~/types";

export const BlogPage = () => {
  const language = useCurrentLanguage();

  const { data, loading } = useBlogIndexQuery({
    variables: {
      language,
    },
  });

  if (loading) {
    return <PageLoading titleId="blog.title" />;
  }

  const posts = data.blogPosts;

  return (
    <Fragment>
      <FormattedMessage id="blog.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Box sx={{ mx: "auto", px: 3, py: 5, maxWidth: "container" }}>
        {posts.map((post) => (
          <Box as="article" key={post.slug} sx={{ mb: 4, maxWidth: "600px" }}>
            <Heading sx={{ mb: 2 }}>
              <Link
                variant="heading"
                path={`/blog/[slug]`}
                params={{ slug: post.slug }}
              >
                {post.title}
              </Link>
            </Heading>

            <Text sx={{ mb: 2 }}>{post.excerpt}</Text>

            <Link path={`/blog/[slug]`} params={{ slug: post.slug }}>
              <FormattedMessage id="blog.readMore" />
            </Link>
          </Box>
        ))}
      </Box>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryBlogIndex(client, {
      language: locale,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default BlogPage;
