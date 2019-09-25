import { graphql } from "gatsby";
import * as React from "react";

import { Hero } from "../components/hero";
import { Events } from "../components/home-events";
import { Faq } from "../components/home-faq";
import { MaxWidthWrapper } from "../components/max-width-wrapper";
import { SponsorList } from "../components/sponsor-list";
import { TwoColumnsText } from "../components/two-columns-text";
import { HomePageQuery } from "../generated/graphql";
import { HomeLayout } from "../layouts/home";

export default ({ data }: { data: HomePageQuery }) => {
  const {
    heroImage,
    backend: { conference },
  } = data;

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
        <Events events={conference.events} />
      </section>
      <section>
        <Faq />
      </section>
    </HomeLayout>
  );
};

export const query = graphql`
  query HomePage($language: String!) {
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
        name(language: $language)
        introduction(language: $language)

        introTitle: copy(key: "intro-title-1", language: $language)
        introText: copy(key: "intro-text-1", language: $language)
        introTitle2: copy(key: "intro-title-2", language: $language)
        introText2: copy(key: "intro-text-2", language: $language)

        events {
          title
          image
          imageFile {
            childImageSharp {
              fluid(
                duotone: { highlight: "#0066FF", shadow: "#0B0040" }
                maxWidth: 600
                maxHeight: 300
                background: "white"
              ) {
                ...GatsbyImageSharpFluid
              }
            }
          }
        }

        sponsorsByLevel {
          level
          sponsors {
            name
            link
            image
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
`;
