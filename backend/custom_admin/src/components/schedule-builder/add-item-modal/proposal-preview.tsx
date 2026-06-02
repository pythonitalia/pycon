import { Badge, Button, Card, Flex, Text } from "@radix-ui/themes";
import type { Language } from "../../../types";
import type { SubmissionFragmentFragment } from "../../fragments/submission.generated";
import type { AvailabilityValue } from "../../utils/availability";
import { getSlotAvailabilityKey } from "../../utils/availability";
import { useCurrentConference } from "../../utils/conference";
import { useAddItemModal } from "./context";
import { useCreateScheduleItemMutation } from "./create-schedule-item.generated";
import { InfoRecap } from "./info-recap";

const AVAILABILITY_BADGE: Record<
  AvailabilityValue,
  { label: string; color: "green" | "blue" | "red" }
> = {
  preferred: { label: "Preferred", color: "green" },
  available: { label: "Available", color: "blue" },
  unavailable: { label: "Unavailable", color: "red" },
};

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
          <Badge color={AVAILABILITY_BADGE[slotAvailability].color}>
            {AVAILABILITY_BADGE[slotAvailability].label}
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
  const languages = proposal.languages;
  const onCreate = async (language: Language) => {
    await createScheduleItem({
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
    close();
  };

  return (
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
  );
};
