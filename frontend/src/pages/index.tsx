import * as React from "react";

import { graphql, useStaticQuery } from "gatsby";
import { Hero } from "../components/hero";
import { Events } from "../components/home-events";
import { Faq } from "../components/home-faq";
import { SponsorList } from "../components/sponsor-list";
import { TwoColumnsText } from "../components/two-columns-text";
import { HomePageQuery } from "../generated/graphql";
import { HomeLayout } from "../layouts/home";

export default () => {
  const {
    heroImage,
    logoImage,
    backend: { conference },
  } = useStaticQuery<HomePageQuery>(graphql`
    query HomePage {
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

      backend {
        conference(code: "pycon10") {
          name
        }
      }
    }
  `);

  const mockSponsors = [
    {
      category: "diversity",
      logos: [
        {
          name: "python",
          logo: logoImage!.childImageSharp!,
          link: "https://www.python.org/",
        },
        {
          name: "python2",
          logo: logoImage!.childImageSharp!,
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
          logo: logoImage!.childImageSharp!,
          link: "https://www.python.org/",
        },
      ],
    },
  ];

  return (
    <HomeLayout>
      <Hero
        title={conference.name}
        backgroundImage={heroImage!.childImageSharp!}
      >
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias et
          omnis hic veniam nisi architecto reprehenderit voluptate magnam sed
          commodi vel quidem ea, blanditiis quos harum non ipsam, soluta saepe.
        </p>
      </Hero>

      <TwoColumnsText />

      <section>
        <SponsorList sponsors={mockSponsors} />
      </section>
      <section>
        <Events />
      </section>
      <section>
        <Faq />
      </section>
    </HomeLayout>
  );
};
