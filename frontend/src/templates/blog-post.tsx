/** @jsx jsx */
import { Box } from "@theme-ui/components";
import { graphql } from "gatsby";
import { Fragment } from "react";
import { Helmet } from "react-helmet";
import { jsx } from "theme-ui";

import { Article } from "../components/article";
import { PostQuery } from "../generated/graphql";
import { compile } from "../helpers/markdown";

export default ({ data }: { data: PostQuery }) => {
  const post = data.backend.blogPost!;

  return (
    <Fragment>
      <Helmet>
        <title>{post.title}</title>
      </Helmet>

      <Box sx={{ mx: "auto", px: 3, maxWidth: "container" }}>
        <Article
          hero={post.imageFile && { ...post.imageFile.childImageSharp! }}
          title={post.title}
        >
          {compile(post.content).tree}
        </Article>
      </Box>
    </Fragment>
  );
};

export const query = graphql`
  query Post($slug: String!, $language: String!) {
    backend {
      blogPost(slug: $slug) {
        title(language: $language)
        content(language: $language)
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
