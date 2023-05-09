import { Page, Section } from "@python-italia/pycon-styleguide";

import { useRouter } from "next/router";

import { useParticipantPublicProfileQuery } from "~/types";

import { ParticipantInfoSection } from "../participant-info-section";

export const PublicProfilePageHandler = () => {
  const router = useRouter();
  const {
    data: { participant },
  } = useParticipantPublicProfileQuery({
    variables: {
      userId: router.query.hashid as string,
      conference: process.env.conferenceCode,
    },
  });
  console.log("participant", participant);

  return (
    <Page endSeparator={false}>
      <Section>
        <ParticipantInfoSection participant={participant} />
      </Section>
    </Page>
  );
};
