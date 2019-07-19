import * as React from "react";

import { graphql } from "gatsby";
import { Article } from "../components/article";
import { ArticleTitle } from "../components/article/title";
import { Column } from "../components/column";
import { Row } from "../components/row";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { HomeLayout } from "../layouts/home";

type BlogPostProps = {
  data: any;
};

export default ({ data }: BlogPostProps) => (
  <HomeLayout>
    <Row paddingLeft={STANDARD_ROW_PADDING} paddingRight={STANDARD_ROW_PADDING}>
      <Column
        colWidth={{
          mobile: 12,
          tabletPortrait: 12,
          tabletLandscape: 12,
          desktop: 8,
        }}
      >
        <Article hero={{ ...data.heroImage.childImageSharp }}>
          <p>
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Saepe,
            illo consequatur numquam, laudantium recusandae sed voluptas odio
            voluptate magni hic omnis vitae mollitia porro eius illum nesciunt
            ad blanditiis maxime!
          </p>
          <p>
            Voluptas quidem accusantium alias quos doloremque, molestiae
            quibusdam nemo iure velit cumque, quas dolore amet est a earum.
            Quisquam amet eius error suscipit voluptate earum dolore ipsam
            asperiores, illo quod!
          </p>
          <p>
            Mollitia, at sit. Magni delectus enim laudantium a odio provident
            eveniet doloremque quisquam molestias ut optio, blanditiis deleniti.
            Maiores officiis distinctio pariatur, excepturi dolorem sapiente
            quisquam facere nesciunt optio error!
          </p>
          <p>
            Qui quas sequi dolorem accusantium fugiat facilis, accusamus, odit
            eligendi rerum ipsum, labore ut perspiciatis molestiae aliquid
            dignissimos minima exercitationem libero quae molestias nesciunt
            veritatis laudantium. Consequatur molestiae similique vel.
          </p>
          <p>
            Quis nemo at ipsum. Accusantium consectetur obcaecati dignissimos
            nisi ad voluptatibus id nesciunt modi vitae enim similique esse
            quasi in, possimus placeat? Unde velit veritatis magnam modi,
            mollitia dolorum omnis!
          </p>
        </Article>
      </Column>
    </Row>
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
