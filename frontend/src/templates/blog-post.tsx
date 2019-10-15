import { graphql } from "gatsby";
import { Column, Container, Row } from "grigliata";
import marksy from "marksy";
import React, { createElement } from "react";

import { Article } from "../components/article";
import { PostQuery } from "../generated/graphql";
import { MainLayout } from "../layouts/main";

const compile = marksy({
  createElement,
});

export default ({
  data,
  pageContext,
}: {
  data: PostQuery;
  pageContext: { language: string };
}) => {
  const post = data.backend.blogPost!;

  return (
    <MainLayout language={pageContext.language}>
      <Container>
        <Row>
          <Column
            columnWidth={{
              mobile: 12,
              tabletPortrait: 12,
              tabletLandscape: 12,
              desktop: 12,
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
      </Container>
    </MainLayout>
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
