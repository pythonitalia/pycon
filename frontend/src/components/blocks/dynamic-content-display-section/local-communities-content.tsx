import {
  CardPart,
  Grid,
  Heading,
  MultiplePartsCard,
  MultiplePartsCardCollection,
  SocialLinks,
  Spacer,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import { Section } from "@python-italia/pycon-styleguide";

export const LocalCommunitiesContent = () => {
  return (
    <Section>
      <Grid cols={3} mdCols={2}>
        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((item) => (
          <MultiplePartsCard>
            <CardPart shrink={false} size="none">
              <img
                style={{
                  objectFit: "cover",
                }}
                alt="test"
                src="https://live.staticflickr.com/65535/54571831519_ed2daa51c6_k.jpg?s=eyJpIjo1NDU3MTgzMTUxOSwiZSI6MTc3MDQ5MjM3NCwicyI6ImE4NjVmZTkwZDAxZTIzMzY4MWM3NDM1OGNmYWYxOGQ3MTYyMDk0NDkiLCJ2IjoxfQ"
              />
            </CardPart>

            <CardPart>
              <Heading size={4}>Python Bari</Heading>
            </CardPart>
            <CardPart background="milk">
              <VerticalStack alignItems="center" gap="small">
                <img
                  src="https://cdn.pycon.it/images/pythonvarese.width-500.png"
                  alt="Python Bari"
                />
              </VerticalStack>
              <Spacer size="small" />
              <Text size={3}>
                Python Bari è una community di Python che si occupa di
                sviluppare software per la città di Bari.
              </Text>
            </CardPart>
            <CardPart background="milk">
              <VerticalStack alignItems="center" gap="small">
                <SocialLinks
                  hoverColor="green"
                  socials={[
                    {
                      icon: "mastodon",
                      link: "https://social.python.it/@pycon",
                      rel: "me",
                    },
                    {
                      icon: "facebook",
                      link: "https://www.facebook.com/pythonitalia",
                      rel: "me",
                    },
                    {
                      icon: "instagram",
                      link: "https://www.instagram.com/pycon.it",
                      rel: "me",
                    },
                    {
                      icon: "linkedin",
                      link: "https://www.linkedin.com/company/pycon-italia",
                      rel: "me",
                    },
                    {
                      icon: "twitter",
                      link: "https://twitter.com/pyconit",
                      rel: "me",
                    },
                  ]}
                />
              </VerticalStack>
            </CardPart>
          </MultiplePartsCard>
        ))}
      </Grid>
    </Section>
  );
};
