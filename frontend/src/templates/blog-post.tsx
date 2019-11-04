import { graphql } from "gatsby";
import marksy from "marksy";
import React, { createElement } from "react";

import { Article } from "../components/article";
import { PostQuery } from "../generated/graphql";

const compile = marksy({
  createElement,
});

export default ({ data }: { data: PostQuery }) => {
  const post = data.backend.blogPost!;

  return (
    <Article
      hero={post.imageFile && { ...post.imageFile.childImageSharp! }}
      title={post.title}
      description={post.excerpt || ""}
    >
      {compile(post.content).tree}
    </Article>
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
