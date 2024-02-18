import {
  Grid,
  GridColumn,
  Heading,
  HorizontalStack,
  LayoutContent,
  Link,
  Spacer,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import {
  FacebookIcon,
  InstagramIcon,
  LinkedinIcon,
  MastodonIcon,
  TwitterIcon,
  WebIcon,
} from "@python-italia/pycon-styleguide/icons";
import { SnakeTail } from "@python-italia/pycon-styleguide/illustrations";
import React from "react";

import { compile } from "~/helpers/markdown";

export type Participant = {
  fullname: string;
  bio: string;
  photo: string;

  twitterHandle?: string;
  instagramHandle?: string;
  mastodonHandle?: string;
  linkedinUrl?: string;
  facebookUrl?: string;
  website?: string;
};

export const ParticipantInfoSection = ({
  participant,
}: {
  participant: Participant;
}) => (
  <>
    <Grid cols={12} mdCols={12}>
      <GridColumn colSpan={4} mdColSpan={4}>
        <LayoutContent position="relative">
          <VerticalStack>
            {participant.photo && (
              <>
                <img
                  alt="Participant"
                  className="aspect-square border-black border z-10 object-cover"
                  src={participant.photo}
                />
                <LayoutContent
                  zIndex={1}
                  style={{ bottom: "-60px", left: "20px" }}
                  showFrom="desktop"
                  position="absolute"
                >
                  <SnakeTail className="w-24" />
                </LayoutContent>
              </>
            )}

            <Spacer size="2md" />
            <HorizontalStack
              alignItems="center"
              justifyContent="end"
              gap="medium"
            >
              {participant.twitterHandle && (
                <Link
                  target="_blank"
                  href={`https://twitter.com/${participant.twitterHandle}`}
                >
                  <TwitterIcon className="w-6 h-6" />
                </Link>
              )}

              {participant.instagramHandle && (
                <Link
                  target="_blank"
                  href={`https://instagram.com/${participant.instagramHandle}`}
                >
                  <InstagramIcon className="w-6 h-6" />
                </Link>
              )}

              {participant.mastodonHandle && (
                <Link
                  target="_blank"
                  href={convertMastodonHandle(participant.mastodonHandle)}
                >
                  <MastodonIcon className="w-6 h-6" />
                </Link>
              )}

              {participant.linkedinUrl && (
                <Link target="_blank" href={participant.linkedinUrl}>
                  <LinkedinIcon className="w-6 h-6" />
                </Link>
              )}

              {participant.facebookUrl && (
                <Link target="_blank" href={participant.facebookUrl}>
                  <FacebookIcon className="w-6 h-6" />
                </Link>
              )}

              {participant.website && (
                <Link target="_blank" href={participant.website}>
                  <WebIcon className="w-6 h-6" />
                </Link>
              )}
            </HorizontalStack>
          </VerticalStack>
        </LayoutContent>
      </GridColumn>
      <GridColumn colSpan={8} mdColSpan={8}>
        <Heading size="display2">{participant.fullname}</Heading>
        <Spacer size="2md" />
        {participant.bio && (
          <Text size={2}>{compile(participant.bio).tree}</Text>
        )}
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
