import {
  CardPart,
  Grid,
  Heading,
  MultiplePartsCard,
  MultiplePartsCardCollection,
  SocialLinks,
  Spacer,
  StyledHTMLText,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import { Section } from "@python-italia/pycon-styleguide";
import type { Community } from "~/types";

type Props = {
  title: string;
  communities: Community[];
};

export const CommunitiesSection = ({ title, communities }: Props) => {
  return (
    <Section>
      <Grid cols={3} mdCols={2}>
        {communities.map((community) => {
          const socialLinks = [];
          if (community.mastodonUrl) {
            socialLinks.push({
              icon: "mastodon",
              link: community.mastodonUrl,
            });
          }
          if (community.facebookUrl) {
            socialLinks.push({
              icon: "facebook",
              link: community.facebookUrl,
            });
          }
          if (community.instagramUrl) {
            socialLinks.push({
              icon: "instagram",
              link: community.instagramUrl,
            });
          }
          if (community.linkedinUrl) {
            socialLinks.push({
              icon: "linkedin",
              link: community.linkedinUrl,
            });
          }
          if (community.twitterUrl) {
            socialLinks.push({
              icon: "twitter",
              link: community.twitterUrl,
            });
          }

          return (
            <MultiplePartsCard>
              <CardPart>
                <Heading size={4}>{community.name}</Heading>
              </CardPart>
              <CardPart background="milk">
                {community.logo && (
                  <>
                    <VerticalStack alignItems="center" gap="small">
                      <img src={community.logo} alt={community.name} />
                    </VerticalStack>
                    <Spacer size="small" />
                  </>
                )}

                <StyledHTMLText text={community.description} baseTextSize={2} />
              </CardPart>
              <CardPart background="milk">
                <VerticalStack alignItems="center" gap="small">
                  <SocialLinks hoverColor="green" socials={socialLinks} />
                </VerticalStack>
              </CardPart>
            </MultiplePartsCard>
          );
        })}
      </Grid>
    </Section>
  );
};
