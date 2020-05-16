/** @jsx jsx */
import { useRouter } from "next/router";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Flex, Grid, jsx, Text } from "theme-ui";

import { Article } from "~/components/article";
import { BlogPostIllustration } from "~/components/illustrations/blog-post";
import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { compile } from "~/helpers/markdown";
import { useCurrentLanguage } from "~/locale/context";
import { usePostQuery } from "~/types";

export default () => {
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
      <MetaTags title={post.title} description={post.excerpt || post.title} />

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
