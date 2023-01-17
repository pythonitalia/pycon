import {
  MultiplePartsCard,
  CardPart,
  Grid,
  Heading,
  Spacer,
  Text,
  GridColumn,
  InputNumber,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { Submission } from "~/types";

type Props = {
  submission: Submission;
};

export const VotingCard = ({ submission }: Props) => {
  return (
    <MultiplePartsCard
      openByDefault={false}
      clickablePart="heading"
      expandTarget="content"
    >
      <CardPart
        contentAlign="left"
        id="heading"
        icon="star"
        noBg
        openLabel={<FormattedMessage id="global.accordion.readMore" />}
      >
        <Heading size={3}>{submission.title}</Heading>
      </CardPart>
      <CardPart id="content" contentAlign="left" noBg>
        <InputNumber
          values={[
            {
              value: "1",
              label: <FormattedMessage id="voteSelector.notInterested" />,
            },
            {
              value: "2",
              label: <FormattedMessage id="voteSelector.maybe" />,
            },
            {
              value: "3",
              label: <FormattedMessage id="voteSelector.wantToSee" />,
            },
            {
              value: "4",
              label: <FormattedMessage id="voteSelector.mustSee" />,
            },
          ]}
        />
      </CardPart>
      <CardPart id="content" contentAlign="left" noBg size="none">
        <Grid cols={2} gap="none" divide={true}>
          <CardPart contentAlign="left" noBg>
            <Text weight="strong" uppercase as="p" size={3}>
              <FormattedMessage id="voting.elevatorPitch" />
            </Text>

            <Spacer size="small" />

            <Text as="p" size={3}>
              {submission.elevatorPitch}
            </Text>
          </CardPart>

          <CardPart contentAlign="left" noBg>
            <Text weight="strong" uppercase as="p" size={3}>
              <FormattedMessage id="voting.tags" />
            </Text>
            <Spacer size="small" />

            <Text weight="strong" as="p" size={3}>
              {submission.tags.map((tag) => tag.name).join(", ")}
            </Text>
          </CardPart>
        </Grid>
      </CardPart>

      <CardPart id="content" contentAlign="left" noBg size="none">
        <Grid cols={3} gap="none" divide={true}>
          <CardPart contentAlign="left" noBg>
            <Text weight="strong" uppercase as="p" size={3}>
              <FormattedMessage id="voting.length" />
            </Text>

            <Spacer size="small" />

            <Text as="p" size={3}>
              <FormattedMessage id="voting.minutes">
                {(text) => (
                  <>
                    {submission.duration.duration} {text}
                  </>
                )}
              </FormattedMessage>
            </Text>
          </CardPart>

          <CardPart contentAlign="left" noBg>
            <Text weight="strong" uppercase as="p" size={3}>
              <FormattedMessage id="voting.audienceLevel" />
            </Text>
            <Spacer size="small" />

            <Text weight="strong" as="p" size={3}>
              {submission.audienceLevel.name}
            </Text>
          </CardPart>

          <CardPart
            contentAlign="left"
            noBg
            rightSideIcon="arrow"
            rightSideIconBackground="none"
          >
            <Text weight="strong" uppercase as="p" size={3}>
              <FormattedMessage id="voting.languages" />
            </Text>
            <Spacer size="small" />

            <Text weight="strong" as="p" size={3}>
              {submission.languages.map((language) => language.name).join(", ")}
            </Text>
          </CardPart>
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
