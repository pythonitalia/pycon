import {
  CardPart,
  Grid,
  Heading,
  HorizontalStack,
  MultiplePartsCard,
  MultiplePartsCardCollection,
  Section,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";
import { VotingCard } from "~/components/voting-card";
import { useCurrentLanguage } from "~/locale/context";
import { useAcceptedProposalsQuery } from "~/types";

export const AcceptedProposalsContent = () => {
  const [filterBy, setFilterBy] = React.useState(null);
  const language = useCurrentLanguage();
  let {
    data: {
      submissions: { items: submissions },
    },
  } = useAcceptedProposalsQuery({
    variables: {
      code: process.env.conferenceCode,
      language,
    },
  });

  if (filterBy === "talks") {
    submissions = submissions.filter(
      (submission) => submission.type.name.toLowerCase() === "talk",
    );
  } else if (filterBy === "workshops") {
    submissions = submissions.filter(
      (submission) => submission.type.name.toLowerCase() === "workshop",
    );
  }

  return (
    <Section>
      <MultiplePartsCardCollection>
        <MultiplePartsCard>
          <CardPart contentAlign="left" overflow={true}>
            <HorizontalStack justifyContent="spaceBetween" alignItems="center">
              <Heading size={2}>
                <FormattedMessage id="voting.proposals" />
              </Heading>
              <VerticalStack alignItems="center" gap="small">
                <Text weight="strong" size="label3">
                  <FormattedMessage id="voting.filterBy" />
                </Text>

                <div className="divide-x divide-black">
                  <Text
                    weight={filterBy === null ? "strong" : null}
                    size="label3"
                    className="pr-2"
                    onClick={() => setFilterBy(null)}
                  >
                    <FormattedMessage id="voting.all" />
                  </Text>
                  <Text
                    weight={filterBy === "talks" ? "strong" : null}
                    size="label3"
                    className="pl-2 pr-2"
                    onClick={() => setFilterBy("talks")}
                  >
                    <FormattedMessage id="voting.talks" />
                  </Text>
                  <Text
                    weight={filterBy === "workshops" ? "strong" : null}
                    size="label3"
                    className="pl-2"
                    onClick={() => setFilterBy("workshops")}
                  >
                    <FormattedMessage id="voting.workshops" />
                  </Text>
                </div>
              </VerticalStack>
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
