import React, { createElement } from "react";

import { graphql } from "gatsby";
import { Column, Row } from "grigliata";
import marksy from "marksy";
import { Article } from "../components/article";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { PageQuery } from "../generated/graphql";
import { HomeLayout } from "../layouts/home";

const compile = marksy({
  createElement,
});

export default ({ data }: { data: PageQuery }) => {
  const page = data.backend.page!;

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
            hero={page.imageFile && { ...page.imageFile.childImageSharp! }}
            title={page.title}
          >
            {compile(page.content).tree}
          </Article>
        </Column>
      </Row>
    </HomeLayout>
  );
};

export const query = graphql`
  query Page($slug: String!) {
    backend {
      page(slug: $slug) {
        title
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
