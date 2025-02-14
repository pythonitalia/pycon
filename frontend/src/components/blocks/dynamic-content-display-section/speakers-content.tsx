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
      a.speaker.fullName.localeCompare(b.speaker.fullName),
    ),
    (submission) => submission.speaker.participant.id,
  );

  return (
    <Section>
      <Grid cols={3}>
        {Object.entries(submissionsBySpeaker).map(
          ([speakerId, submissions]) => (
            <Link noHover href={`/profile/${speakerId}`} key={speakerId}>
              <SpeakerCard
                speakerName={submissions[0].speaker.fullName}
                portraitUrl={submissions[0].speaker.participant.photo}
                sessions={submissions
                  .map((submission) => submission.title)
                  .join(", ")}
              />
            </Link>
          ),
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
