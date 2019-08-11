"use strict";
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const React = __importStar(require("react"));
const gatsby_1 = require("gatsby");
const hero_1 = require("../components/hero");
const home_events_1 = require("../components/home-events");
const home_faq_1 = require("../components/home-faq");
const sponsor_list_1 = require("../components/sponsor-list");
const two_columns_text_1 = require("../components/two-columns-text");
const home_1 = require("../layouts/home");
exports.default = ({ data }) => {
    const mockSponsors = [
        {
            category: "diversity",
            logos: [
                {
                    name: "python",
                    logo: data.logoImage.childImageSharp,
                    link: "https://www.python.org/",
                },
                {
                    name: "python2",
                    logo: data.logoImage.childImageSharp,
                    category: "diversity",
                    link: "https://www.python.org/",
                },
            ],
        },
        {
            category: "beginner",
            logos: [
                {
                    name: "python3",
                    logo: data.logoImage.childImageSharp,
                    link: "https://www.python.org/",
                },
            ],
        },
    ];
    return (<home_1.HomeLayout>
      <hero_1.Hero title="Pycon XI" backgroundImage={data.heroImage.childImageSharp}>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias et
          omnis hic veniam nisi architecto reprehenderit voluptate magnam sed
          commodi vel quidem ea, blanditiis quos harum non ipsam, soluta saepe.
        </p>
      </hero_1.Hero>

      <two_columns_text_1.TwoColumnsText />

      <section>
        <sponsor_list_1.SponsorList sponsors={mockSponsors}/>
      </section>
      <section>
        <home_events_1.Events />
      </section>
      <section>
        <home_faq_1.Faq />
      </section>
    </home_1.HomeLayout>);
};
exports.query = gatsby_1.graphql `
  query {
    heroImage: file(relativePath: { eq: "images/hero.jpg" }) {
      childImageSharp {
        fluid(maxWidth: 1600) {
          ...GatsbyImageSharpFluid
        }
      }
    }
    logoImage: file(relativePath: { eq: "images/python-logo.png" }) {
      childImageSharp {
        fluid(maxWidth: 1200) {
          ...GatsbyImageSharpFluid
        }
      }
    }
  }
`;
