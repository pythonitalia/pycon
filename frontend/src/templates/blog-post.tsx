/** @jsx jsx */
import { Box } from "@theme-ui/components";
import { graphql } from "gatsby";
import marksy from "marksy";
import { createElement } from "react";
import { jsx } from "theme-ui";

import { Article } from "../components/article";
import { PostQuery } from "../generated/graphql";

const compile = marksy({
  createElement,
});

export default ({ data }: { data: PostQuery }) => {
  const post = data.backend.blogPost!;

  return (
    <Box sx={{ mx: "auto", px: 3, maxWidth: "container" }}>
      <Article
        hero={post.imageFile && { ...post.imageFile.childImageSharp! }}
        title={post.title}
      >
        {compile(post.content).tree}
      </Article>
    </Box>
  );
};

export const query = graphql`
  query Post($slug: String!) {
    backend {
      blogPost(slug: $slug) {
        title
        excerpt
        content
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
