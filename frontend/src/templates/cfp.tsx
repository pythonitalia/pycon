import React from "react";

import { graphql } from "gatsby";
import { Column, Container, Row } from "grigliata";
import { Article } from "../components/article";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { MainLayout } from "../layouts/main";
import { CFPForm } from "../routes/cfp/form";
import { CfpQuery } from "../generated/graphql";

export default ({ data, pageContext }: { data: CfpQuery, pageContext: { language: string } }) => {
  console.log(pageContext);
  return (
    <MainLayout language={pageContext.language}>
      <Container fullWidth={false}>
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
              hero={{ ...data.heroImage.childImageSharp }}
              title="Call For Proposal"
            >
              <CFPForm/>
            </Article>
          </Column>
        </Row>
      </Container>
    </MainLayout>
  );
};

export const query = graphql`
    query Cfp{
        heroImage: file(relativePath: { eq: "images/cfp.jpg" }) {
            childImageSharp {
                fluid(maxWidth: 1600) {
                    ...GatsbyImageSharpFluid
                }
            }
        }
    }
`;
