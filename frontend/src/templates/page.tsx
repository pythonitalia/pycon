import { graphql } from "gatsby";
import { Column, Container, Row } from "grigliata";
import marksy from "marksy";
import React, { createElement } from "react";

import { Article } from "../components/article";
import { MaxWidthWrapper } from "../components/max-width-wrapper";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { PageQuery } from "../generated/graphql";
import { MainLayout } from "../layouts/main";

const compile = marksy({
  createElement,
});

export default ({
  data,
  pageContext,
}: {
  data: PageQuery;
  pageContext: { language: string };
}) => {
  const page = data.backend.page!;

  return (
    <MainLayout language={pageContext.language}>
      <Container>
        <Row
          paddingLeft={STANDARD_ROW_PADDING}
          paddingRight={STANDARD_ROW_PADDING}
        >
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
      </Container>
    </MainLayout>
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
            fluid(
              maxWidth: 1600
              maxHeight: 700
              fit: COVER
              cropFocus: ATTENTION
              duotone: { highlight: "#000000", shadow: "#000000", opacity: 20 }
            ) {
              ...GatsbyImageSharpFluid
            }
          }
        }
      }
    }
  }
`;
