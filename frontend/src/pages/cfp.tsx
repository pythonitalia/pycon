import React  from "react";

import { graphql } from "gatsby";
import { Column, Container, Row } from "grigliata";
import { Article } from "../components/article";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { HomeLayout } from "../layouts/home";
import { CFPForm } from "../routes/cfp/form";

type CfpProps = {
  data: any;
};

export default ({ data }: CfpProps) => (
  <HomeLayout>
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
  </HomeLayout>
);

export const query = graphql`
  query {
    heroImage: file(relativePath: { eq: "images/cfp.jpg" }) {
      childImageSharp {
        fluid(maxWidth: 1600) {
          ...GatsbyImageSharpFluid
        }
      }
    }
  }
`;
