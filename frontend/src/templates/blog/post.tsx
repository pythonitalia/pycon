/** @jsx jsx */
import { Box, Flex, Grid, Text } from "@theme-ui/components";
import { graphql } from "gatsby";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { Article } from "../../components/article";
import { BlogPostIllustration } from "../../components/illustrations/blog-post";
import { MetaTags } from "../../components/meta-tags";
import { PostQuery } from "../../generated/graphql";
import { compile } from "../../helpers/markdown";

type Props = {
  data: PostQuery;
  pageContext: {
    socialCard: string;
  };
};

export default ({ data, ...props }: Props) => {
  const post = data.backend.blogPost!;
  const socialCard = `${data.site!.siteMetadata!.siteUrl}${
    props.pageContext.socialCard
  }`;

  return (
    <Fragment>
      <MetaTags
        title={post.title}
        description={post.excerpt || post.title}
        imageUrl={socialCard}
      />

      <Grid
        sx={{
          mx: "auto",
          px: 3,
          py: 5,
          maxWidth: "container",
          gridColumnGap: 5,
          gridTemplateColumns: [null, null, "2fr 1fr"],
        }}
      >
        <Box>
          <Article
            hero={post.imageFile && { ...post.imageFile.childImageSharp! }}
            published={post.published}
            title={post.title}
          >
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

export const query = graphql`
  query Post($slug: String!, $language: String!) {
    site {
      siteMetadata {
        siteUrl
      }
    }

    backend {
      blogPost(slug: $slug) {
        title(language: $language)
        content(language: $language)
        excerpt(language: $language)
        author {
          fullName
        }
        published
        image

        imageFile {
          childImageSharp {
            fluid(maxWidth: 1600) {
              ...GatsbyImageSharpFluid
            }
          }
        }
      }
    }
  }
`;
