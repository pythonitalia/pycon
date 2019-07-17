import * as React from "react";

import { graphql } from "gatsby";
import { Hero } from "../components/hero";
import { SectionTitle } from "../components/section-title";
import { TwoColumnsText } from "../components/two-columns-text";
import { HomeLayout } from "../layouts/home";

type HomeProps = {
  data: any;
};

export default ({ data }: HomeProps) => (
  <HomeLayout>
    <Hero title="Pycon XI" backgroundImage={data.heroImage.childImageSharp}>
      <p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias et omnis
        hic veniam nisi architecto reprehenderit voluptate magnam sed commodi
        vel quidem ea, blanditiis quos harum non ipsam, soluta saepe.
      </p>
    </Hero>

    <TwoColumnsText />

    <section>
      <SectionTitle>Sponsors</SectionTitle>
    </section>
  </HomeLayout>
);

export const query = graphql`
  query {
    heroImage: file(relativePath: { eq: "images/hero.jpg" }) {
      childImageSharp {
        fluid(maxWidth: 1600) {
          ...GatsbyImageSharpFluid
        }
      }
    }
  }
`;
