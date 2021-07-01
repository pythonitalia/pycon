/** @jsxRuntime classic */
/** @jsx jsx */
import { GetStaticProps, GetStaticPaths } from "next";
import { useRouter } from "next/router";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Flex, Grid, jsx, Text } from "theme-ui";
import { addApolloState } from "~/apollo/client";

import { Article } from "~/components/article";
import { BlogPostIllustration } from "~/components/illustrations/blog-post";
import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { compile } from "~/helpers/markdown";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryBlogIndex, queryPost, usePostQuery } from "~/types";

export const BlogArticlePage = () => {
  const language = useCurrentLanguage();
  const router = useRouter();
  const slug = router.query.slug as string;

  const { data, loading } = usePostQuery({
    variables: {
      language,
      slug,
    },
  });

  if (loading) {
    return <PageLoading titleId="global.loading" />;
  }

  const post = data.blogPost;

  return (
    <Fragment>
      <MetaTags
        title={post.title}
        description={post.excerpt || post.title}
        useDefaultSocialCard={false}
      />

      <Grid
        gap={5}
        sx={{
          mx: "auto",
          px: 3,
          py: 5,
          maxWidth: "container",
          gridTemplateColumns: [null, null, "2fr 1fr"],
        }}
      >
        <Box>
          <Article published={post.published} title={post.title}>
            {compile(post.content).tree}
          </Article>
        </Box>

        <Box>
          <Flex
            sx={{
              position: "relative",
              justifyContent: "flex-end",
              alignItems: "flex-start",
            }}
          >
            <BlogPostIllustration
              sx={{
                width: "80%",
              }}
            />

            <Box
              sx={{
                border: "primary",
                p: 4,
                backgroundColor: "cinderella",
                width: "80%",
                position: "absolute",
                left: 0,
                top: "70%",
              }}
            >
              <Text sx={{ fontWeight: "bold" }}>
                <FormattedMessage id="blog.author" />
              </Text>

              <Text>{post.author.fullName}</Text>
            </Box>
          </Flex>
        </Box>
      </Grid>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const language = params.lang as string;
  const slug = params.slug as string;

  await prefetchSharedQueries(language);

  await queryPost({
    slug,
    language,
  });

  return addApolloState({
    props: {},
    revalidate: 1,
  });
};

export const getStaticPaths: GetStaticPaths = async () => {
  const {
    data: { blogPosts: italianBlogPosts },
  } = await queryBlogIndex({
    language: "it",
  });

  const {
    data: { blogPosts: englishBlogPosts },
  } = await queryBlogIndex({
    language: "en",
  });

  const paths = [
    ...italianBlogPosts.map((blogPost) => ({
      params: {
        lang: "it",
        slug: blogPost.slug,
      },
    })),
    ...englishBlogPosts.map((blogPost) => ({
      params: {
        lang: "en",
        slug: blogPost.slug,
      },
    })),
  ];

  return {
    paths,
    fallback: false,
  };
};

export default BlogArticlePage;
