import {
  Grid,
  Link,
  Section,
  SpeakerCard,
} from "@python-italia/pycon-styleguide";

import { useCurrentLanguage } from "~/locale/context";
import { useAcceptedProposalsQuery } from "~/types";

export const SpeakersContent = () => {
  const language = useCurrentLanguage();
  const {
    data: {
      conference: { submissions },
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
                  talkTitle={title}
                  speakerName={submissions[0].speaker.fullname}
                  portraitUrl={submissions[0].speaker.photo}
                />
              </Link>
            );
          },
        )}
      </Grid>
    </Section>
  );
};
