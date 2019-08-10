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
            hero={{ ...data.heroImage!.childImageSharp }}
            title={post.title}
            description={post.excerpt}
          >
            {compile(post.content).tree}
          </Article>
        </Column>
      </Row>
    </HomeLayout>
  );
};

export const query = graphql`
  query Post {
    backend {
      blogPost(slug: "hello-world") {
        title
        excerpt
        content
      }
    }

    heroImage: file(relativePath: { eq: "images/hero.jpg" }) {
      childImageSharp {
        fluid(maxWidth: 1600) {
          ...GatsbyImageSharpFluid
        }
      }
    }
  }
`;
