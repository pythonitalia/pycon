import {
  Grid,
  Link,
  Heading,
  GridColumn,
  VerticalStack,
  Spacer,
  HorizontalStack,
  Text,
  LayoutContent,
} from "@python-italia/pycon-styleguide";
import {
  TwitterIcon,
  InstagramIcon,
  MastodonIcon,
  LinkedinIcon,
  FacebookIcon,
  WebIcon,
} from "@python-italia/pycon-styleguide/icons";
import { SnakeTail } from "@python-italia/pycon-styleguide/illustrations";
import React from "react";

import { compile } from "~/helpers/markdown";

export type Speaker = {
  name: string;
  bio: string;
  photo: string;

  twitterHandle?: string;
  instagramHandle?: string;
  mastodonHandle?: string;
  linkedinUrl?: string;
  facebookUrl?: string;
  website?: string;
};

export const SpeakerSection = ({ speaker }: { speaker: Speaker }) => (
  <>
    <Grid cols={12} mdCols={12}>
      <GridColumn colSpan={4} mdColSpan={4}>
        <LayoutContent position="relative">
          <VerticalStack>
            <img
              alt="speaker photo"
              className="aspect-square border-black border z-10 object-cover"
              src={speaker.photo}
            />
            <LayoutContent
              zIndex={1}
              style={{ bottom: "-60px", left: "20px" }}
              showFrom="desktop"
              position="absolute"
            >
              <SnakeTail className="w-24" />
            </LayoutContent>
            <Spacer size="2md" />
            <HorizontalStack
              alignItems="center"
              justifyContent="end"
              gap="medium"
            >
              {speaker.twitterHandle && (
                <Link
                  target="_blank"
                  href={`https://twitter.com/${speaker.twitterHandle}`}
                >
                  <TwitterIcon className="w-6 h-6" />
                </Link>
              )}

              {speaker.instagramHandle && (
                <Link
                  target="_blank"
                  href={`https://instagram.com/${speaker.instagramHandle}`}
                >
                  <InstagramIcon className="w-6 h-6" />
                </Link>
              )}

              {speaker.mastodonHandle && (
                <Link
                  target="_blank"
                  href={convertMastodonHandle(speaker.mastodonHandle)}
                >
                  <MastodonIcon className="w-6 h-6" />
                </Link>
              )}

              {speaker.linkedinUrl && (
                <Link target="_blank" href={speaker.linkedinUrl}>
                  <LinkedinIcon className="w-6 h-6" />
                </Link>
              )}

              {speaker.facebookUrl && (
                <Link target="_blank" href={speaker.facebookUrl}>
                  <FacebookIcon className="w-6 h-6" />
                </Link>
              )}

              {speaker.website && (
                <Link target="_blank" href={speaker.website}>
                  <WebIcon className="w-6 h-6" />
                </Link>
              )}
            </HorizontalStack>
          </VerticalStack>
        </LayoutContent>
      </GridColumn>
      <GridColumn colSpan={8} mdColSpan={8}>
        <Heading size="display2">{speaker.name}</Heading>
        <Spacer size="2md" />
        <Text size={2}>{compile(speaker.bio).tree}</Text>
      </GridColumn>
    </Grid>
  </>
);

const convertMastodonHandle = (handle: string) => {
  if (handle.startsWith("https://") || handle.startsWith("http://")) {
    return handle;
  }

  const parts = handle.startsWith("@")
    ? handle.substring(1).split("@")
    : handle.split("@");

  return `https://${parts[1]}/@${parts[0]}`;
};
