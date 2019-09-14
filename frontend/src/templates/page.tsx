import { graphql } from "gatsby";
import { Column, Row } from "grigliata";
import marksy from "marksy";
import React, { createElement } from "react";

import { Article } from "../components/article";
import { MaxWidthWrapper } from "../components/max-width-wrapper";
import { PageQuery } from "../generated/graphql";
import { HomeLayout } from "../layouts/home";

const compile = marksy({
  createElement,
});

export default ({ data }: { data: PageQuery }) => {
  const page = data.backend.page!;

  return (
    <HomeLayout>
      <MaxWidthWrapper>
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
              hero={page.imageFile && { ...page.imageFile.childImageSharp! }}
              title={page.title}
            >
              {compile(page.content).tree}
            </Article>
          </Column>
        </Row>
      </MaxWidthWrapper>
    </HomeLayout>
  );
};

export const query = graphql`
  query Page($slug: String!, $language: String!) {
    backend {
      page(slug: $slug) {
        title(language: $language)
        content(language: $language)
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
