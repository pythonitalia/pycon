import { graphql, useStaticQuery } from "gatsby";
import * as React from "react";

import { Hero } from "../components/hero";
import { Events } from "../components/home-events";
import { Faq } from "../components/home-faq";
import { MaxWidthWrapper } from "../components/max-width-wrapper";
import { SponsorList } from "../components/sponsor-list";
import { TwoColumnsText } from "../components/two-columns-text";
import { HomeQuery } from "../generated/graphql";
import { HomeLayout } from "../layouts/home";

export default () => {
  const {
    heroImage,
    backend: { conference },
  } = useStaticQuery<HomeQuery>(graphql`
    query Home {
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
        conference {
          name
          introduction

          introTitle: copy(key: "intro-title-1")
          introText: copy(key: "intro-text-1")
          introTitle2: copy(key: "intro-title-2")
          introText2: copy(key: "intro-text-2")

          sponsorsByLevel {
            level
            sponsors {
              name
              image
              link
              imageFile {
                childImageSharp {
                  fluid(
                    fit: CONTAIN
                    maxWidth: 600
                    maxHeight: 300
                    background: "white"
                  ) {
                    ...GatsbyImageSharpFluid
                  }
                }
              }
            }
          }
        }
      }
    }
  `);

  return (
    <HomeLayout>
      <MaxWidthWrapper>
        <Hero
          title={conference.name}
          backgroundImage={heroImage!.childImageSharp!}
        >
          <p>{conference.introduction}</p>
        </Hero>
      </MaxWidthWrapper>

      <TwoColumnsText
        left={{
          title: conference.introTitle!,
          text: conference.introText!,
        }}
        right={{
          title: conference.introTitle2!,
          text: conference.introText2!,
        }}
      />

      <section>
        <SponsorList sponsors={conference.sponsorsByLevel!} />
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
