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
  return (
    <Section>
      <Grid cols={3}>
        {submissions
          .filter((submission) => submission.speaker)
          .sort((a, b) => a.speaker.fullname.localeCompare(b.speaker.fullname))
          .map((submission) => (
            <Link
              noHover
              href={`/profile/${submission.speaker.id}`}
              key={submission.id}
            >
              <SpeakerCard
                talkTitle={submission.title}
                speakerName={submission.speaker.fullname}
                portraitUrl={submission.speaker.photo}
              />
            </Link>
          ))}
      </Grid>
    </Section>
  );
};
