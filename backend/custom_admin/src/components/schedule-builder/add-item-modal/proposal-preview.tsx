import { Badge, Button, Callout, Card, Flex, Text } from "@radix-ui/themes";
import { useState } from "react";
import type { Language } from "../../../types";
import type { SubmissionFragmentFragment } from "../../fragments/submission.generated";
import type { AvailabilityValue } from "../../utils/availability";
import {
  AVAILABILITY_META,
  getSlotAvailabilityKey,
} from "../../utils/availability";
import { useCurrentConference } from "../../utils/conference";
import { useAddItemModal } from "./context";
import { useCreateScheduleItemMutation } from "./create-schedule-item.generated";
import { InfoRecap } from "./info-recap";

type Props = {
  proposal: SubmissionFragmentFragment;
};

export const ProposalPreview = ({ proposal }: Props) => {
  const { data } = useAddItemModal();

  const availabilityKey =
    data?.day?.day && data?.slot?.hour
      ? getSlotAvailabilityKey(data.day.day, data.slot.hour)
      : null;

  const availabilities: Record<string, AvailabilityValue> =
    proposal.speaker?.participant?.speakerAvailabilities ?? {};

  const slotAvailability = availabilityKey
    ? availabilities[availabilityKey]
    : undefined;

  return (
    <Card>
      <Flex align="start" justify="between" gap="2">
        <div>
          <Text as="div" weight="bold">
            {proposal.title}
          </Text>
          {proposal.italianTitle !== proposal.title && (
            <Text as="div" color="gray">
              {proposal.italianTitle}
            </Text>
          )}
        </div>
        {slotAvailability && (
          <Badge color={AVAILABILITY_META[slotAvailability].color}>
            {AVAILABILITY_META[slotAvailability].label}
          </Badge>
        )}
      </Flex>

      <InfoRecap
        info={[
          { label: "Type", value: proposal.type.name },
          { label: "Duration", value: `${proposal.duration.duration} mins` },
          { label: "Speaker", value: proposal.speaker.fullName },
        ]}
      />
      <AddActions proposal={proposal} />
    </Card>
  );
};

const AddActions = ({ proposal }: { proposal: SubmissionFragmentFragment }) => {
  const { conferenceId } = useCurrentConference();
  const { data, close } = useAddItemModal();
  const [createScheduleItem] = useCreateScheduleItemMutation();
  const [error, setError] = useState<string | null>(null);
  const languages = proposal.languages;
  const onCreate = async (language: Language) => {
    setError(null);
    try {
      const { errors } = await createScheduleItem({
        variables: {
          input: {
            conferenceId,
            type:
              proposal.type.name.toLowerCase() === "talk" ? "talk" : "training",
            proposalId: proposal.id,
            languageId: language.id,
            slotId: data.slot.id,
            rooms: [data.room.id],
          },
        },
      });
      if (errors?.length) {
        setError("Could not add to the schedule. Please try again.");
        return;
      }
      close();
    } catch {
      setError("Could not add to the schedule. Please try again.");
    }
  };

  return (
    <Flex direction="column" gap="2">
      <Flex gap="2" wrap="wrap">
        {languages.map((language) => (
          <Button
            type="button"
            onClick={() => onCreate(language)}
            key={language.id}
          >
            Add to schedule in {language.name}
          </Button>
        ))}
      </Flex>
      {error && (
        <Callout.Root color="red" size="1">
          <Callout.Text>{error}</Callout.Text>
        </Callout.Root>
      )}
    </Flex>
  );
};
