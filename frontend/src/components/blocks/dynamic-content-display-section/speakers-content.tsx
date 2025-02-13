import {
  CardPart,
  Grid,
  Heading,
  Link,
  MultiplePartsCard,
  Section,
  Text,
} from "@python-italia/pycon-styleguide";

import { useCurrentLanguage } from "~/locale/context";
import { useAcceptedProposalsQuery } from "~/types";

export const SpeakersContent = () => {
  const language = useCurrentLanguage();
  const {
    data: {
      submissions: { items: submissions },
    },
  } = useAcceptedProposalsQuery({
    variables: {
      code: process.env.conferenceCode,
      language,
    },
  });

  const submissionsBySpeaker = Object.groupBy(
    submissions.toSorted((a, b) =>
      a.speaker.fullname.localeCompare(b.speaker.fullname),
    ),
    (submission) => submission.speaker.id,
  );

  return (
    <Section>
      <Grid cols={3}>
        {Object.entries(submissionsBySpeaker).map(
          ([speakerId, submissions]) => {
            let title = submissions[0].title;
            if (submissions.length > 1) {
              title = `${title} (+${submissions.length - 1})`;
            }
            return (
              <Link noHover href={`/profile/${speakerId}`} key={speakerId}>
                <SpeakerCard
                  speakerName={submissions[0].speaker.fullname}
                  portraitUrl={submissions[0].speaker.photo}
                  sessions={title}
                />
              </Link>
            );
          },
        )}
      </Grid>
    </Section>
  );
};

const SpeakerCard = ({ portraitUrl, speakerName, sessions }) => (
  <MultiplePartsCard>
    <CardPart shrink={false} size="none">
      <img
        style={{
          objectFit: "cover",
        }}
        className="w-full aspect-[1/0.74]"
        src={portraitUrl}
        alt="speaker portrait"
      />
    </CardPart>
    <CardPart fullHeight contentAlign="left">
      <Heading size={4}>{speakerName}</Heading>
    </CardPart>
    <CardPart shrink={false} background="milk" contentAlign="left">
      <Text size={3}>{sessions}</Text>
    </CardPart>
  </MultiplePartsCard>
);
