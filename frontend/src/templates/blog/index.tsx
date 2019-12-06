/** @jsx jsx */
import { Box, Heading, Text } from "@theme-ui/components";
import { graphql } from "gatsby";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { Link } from "../../components/link";
import { MetaTags } from "../../components/meta-tags";
import { BlogIndexQuery } from "../../generated/graphql";

export default ({ data }: { data: BlogIndexQuery }) => {
  const posts = data.backend.blogPosts;

  return (
    <Fragment>
      <MetaTags title="Blog" />

      <Box sx={{ mx: "auto", px: 3, pt: 4, maxWidth: "container" }}>
        {posts.map(post => (
          <Box as="article" key={post.slug} sx={{ mb: 4, maxWidth: "600px" }}>
            <Heading sx={{ mb: 2 }}>
              <Link variant="heading" href={`/:language/blog/${post.slug}`}>
                {post.title}
              </Link>
            </Heading>

            <Text sx={{ mb: 2 }}>{post.excerpt}</Text>

            <Link href={`/:language/blog/${post.slug}`}>
              <FormattedMessage id="blog.readMore" />
            </Link>
          </Box>
        ))}
      </Box>
    </Fragment>
  );
};

export const query = graphql`
  query BlogIndex($language: String!) {
    backend {
      blogPosts {
        id
        slug
        title(language: $language)
        excerpt(language: $language)
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
