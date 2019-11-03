import { graphql } from "gatsby";
import { Container } from "grigliata";
import * as React from "react";

import { Deadlines } from "../components/deadlines";
import { Hero } from "../components/hero";
import { Events } from "../components/home-events";
import { Faqs } from "../components/home-faq";
import { Marquee } from "../components/marquee";
import {
  HomeMaxWidthWrapper,
  MaxWidthWrapper,
} from "../components/max-width-wrapper";
import { SponsorList } from "../components/sponsor-list";
import { TwoColumnsText } from "../components/two-columns-text";
import { HomePageQuery } from "../generated/graphql";
import { MainLayout } from "../layouts/main";

export default ({
  data,
  pageContext,
}: {
  data: HomePageQuery;
  pageContext: { language: string };
}) => {
  const {
    heroImage,
    backend: { conference },
  } = data;

  return (
    <>
      <Marquee message="Hello world" />
    </>
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
        eventsIntro: copy(key: "events-intro", language: $language)
        deadlinesIntro: copy(key: "deadlines-intro", language: $language)

        deadlines {
          name(language: $language)
          description(language: $language)
          start
          end
        }

        faqs {
          question(language: $language)
          answer(language: $language)
        }

        events {
          title
          locationName
          image
          start
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
