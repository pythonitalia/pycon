/** @jsxRuntime classic */
/** @jsx jsx */
import { GetStaticProps, GetStaticPaths } from "next";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx, Text } from "theme-ui";
import { addApolloState } from "~/apollo/client";

import { Link } from "~/components/link";
import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryBlogIndex, useBlogIndexQuery } from "~/types";

export const BlogPage = () => {
  const language = useCurrentLanguage();

  const { data, loading, error } = useBlogIndexQuery({
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
                path={`/[lang]/blog/[slug]`}
                params={{ slug: post.slug }}
              >
                {post.title}
              </Link>
            </Heading>

            <Text sx={{ mb: 2 }}>{post.excerpt}</Text>

            <Link path={`/[lang]/blog/[slug]`} params={{ slug: post.slug }}>
              <FormattedMessage id="blog.readMore" />
            </Link>
          </Box>
        ))}
      </Box>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const language = params.lang as string;
  await prefetchSharedQueries(language);

  await queryBlogIndex({
    language,
  });

  return addApolloState({
    props: {},
    revalidate: 1,
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default BlogPage;
