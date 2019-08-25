import React, { createElement } from "react";

import { graphql } from "gatsby";
import { Column, Row } from "grigliata";
import marksy from "marksy";
import { Article } from "../components/article";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { PostQuery } from "../generated/graphql";
import { HomeLayout } from "../layouts/home";

const compile = marksy({
  createElement,
});

export default ({ data }: { data: PostQuery }) => {
  const post = data.backend.blogPost!;

  console.log(post);

  return (
    <HomeLayout>
      <Row
        paddingLeft={STANDARD_ROW_PADDING}
        paddingRight={STANDARD_ROW_PADDING}
      >
        <Column
          columnWidth={{
            mobile: 12,
            tabletPortrait: 12,
            tabletLandscape: 12,
            desktop: 8,
          }}
        >
          <Article
            hero={post.imageFile && { ...post.imageFile.childImageSharp! }}
            title={post.title}
            description={post.excerpt || ""}
          >
            {compile(post.content).tree}
          </Article>
        </Column>
      </Row>
    </HomeLayout>
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
