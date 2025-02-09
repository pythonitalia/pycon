import {
  CardPart,
  Heading,
  Link,
  MultiplePartsCard,
  MultiplePartsCardCollection,
  Page,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";

import { useRouter } from "next/router";

import {
  Participant,
  type ParticipantPublicProfileQueryResult,
  useParticipantPublicProfileQuery,
} from "~/types";

import { FormattedMessage } from "react-intl";
import { useCurrentLanguage } from "~/locale/context";
import { createHref } from "../link";
import { ParticipantInfoSection } from "../participant-info-section";
import { ScheduleItemList } from "../schedule-view/schedule-list";

export const PublicProfilePageHandler = () => {
  const router = useRouter();
  const language = useCurrentLanguage();
  const {
    data: { participant },
  } = useParticipantPublicProfileQuery({
    variables: {
      id: router.query.hashid as string,
      conference: process.env.conferenceCode,
      language,
    },
  });

  return (
    <Page endSeparator={false}>
      <Section>
        <ParticipantInfoSection
          fullname={participant.fullname}
          participant={participant}
        />
      </Section>
      {participant.proposals.length > 0 && (
        <Section>
          <Heading size={2}>
            <FormattedMessage id="global.sessions" />
          </Heading>
          <Spacer size="2md" />
          <MultiplePartsCardCollection>
            {participant.proposals.map((proposal) => (
              <ProposalCard proposal={proposal} />
            ))}
          </MultiplePartsCardCollection>
        </Section>
      )}
    </Page>
  );
};

const ProposalCard = ({
  proposal,
}: {
  proposal: ParticipantPublicProfileQueryResult["data"]["participant"]["proposals"][0];
}) => {
  const language = useCurrentLanguage();
  return (
    <MultiplePartsCard>
      <CardPart contentAlign="left">
        <div className="flex flex-row items-center md:gap-3 lg:gap-6">
          <Text size={3} color="grey-500">
            <FormattedMessage
              id="voting.minutes"
              values={{
                type: proposal.type.name,
                duration: proposal.duration.duration,
              }}
            />
            , {proposal.audienceLevel.name}
          </Text>
        </div>
        <Spacer size="xs" />

        <Link
          href={createHref({
            path:
              proposal.scheduleItems.length > 0
                ? `/event/${proposal.scheduleItems[0].slug}`
                : `/submission/${proposal.id}`,
            locale: language,
          })}
        >
          <Heading color="none" size={4}>
            {proposal.title}
          </Heading>
        </Link>
      </CardPart>
    </MultiplePartsCard>
  );
};
