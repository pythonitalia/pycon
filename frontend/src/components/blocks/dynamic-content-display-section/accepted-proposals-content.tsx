import {
  CardPart,
  Heading,
  HorizontalStack,
  MultiplePartsCard,
  MultiplePartsCardCollection,
  Section,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { VotingCard } from "~/components/voting-card";
import { useCurrentLanguage } from "~/locale/context";
import { useAcceptedProposalsQuery } from "~/types";

export const AcceptedProposalsContent = () => {
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

  return (
    <Section>
      <MultiplePartsCardCollection>
        <MultiplePartsCard>
          <CardPart contentAlign="left" overflow={true}>
            <HorizontalStack justifyContent="spaceBetween" alignItems="center">
              <Heading size={2}>
                <FormattedMessage id="voting.proposals" />
              </Heading>
            </HorizontalStack>
          </CardPart>
        </MultiplePartsCard>
        {submissions.map((submission) => (
          <VotingCard
            key={submission.id}
            submission={submission}
            showVotingUI={false}
          />
        ))}
      </MultiplePartsCardCollection>
    </Section>
  );
};
