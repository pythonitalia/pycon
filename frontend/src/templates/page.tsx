import { graphql } from "gatsby";
import { Column, Row } from "grigliata";
import marksy from "marksy";
import React, { createElement } from "react";

import { Article } from "../components/article";
import { MaxWidthWrapper } from "../components/max-width-wrapper";
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
