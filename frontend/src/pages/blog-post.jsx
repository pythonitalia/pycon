"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const gatsby_1 = require("gatsby");
const grigliata_1 = require("grigliata");
const article_1 = require("../components/article");
const spacing_1 = require("../config/spacing");
const home_1 = require("../layouts/home");
exports.default = ({ data }) => (<home_1.HomeLayout>
    <grigliata_1.Row paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
      <grigliata_1.Column columnWidth={{
    mobile: 12,
    tabletPortrait: 12,
    tabletLandscape: 12,
    desktop: 8,
}}>
        <article_1.Article hero={{ ...data.heroImage.childImageSharp }} title="Pycon XI" description="PyCon Italia is the national conference where professionals,
        researchers and enthusiasts of the most beautiful programming language gather together.
        In the wonderful setting of Florence, PyCon is a weekend for learning, meeting and discovering.">
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
        </article_1.Article>
      </grigliata_1.Column>
    </grigliata_1.Row>
  </home_1.HomeLayout>);
exports.query = gatsby_1.graphql `
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
