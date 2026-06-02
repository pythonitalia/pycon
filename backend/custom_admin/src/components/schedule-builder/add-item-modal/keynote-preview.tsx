import { Button, Callout, Card, Text } from "@radix-ui/themes";
import { useState } from "react";
import type { KeynoteFragmentFragment } from "../../fragments/keynote.generated";
import { useCurrentConference } from "../../utils/conference";
import { useAddItemModal } from "./context";
import { useCreateScheduleItemMutation } from "./create-schedule-item.generated";
import { InfoRecap } from "./info-recap";

export const KeynotePreview = ({
  keynote,
}: {
  keynote: KeynoteFragmentFragment;
}) => {
  const { conferenceId } = useCurrentConference();
  const { data, close } = useAddItemModal();
  const [createScheduleItem] = useCreateScheduleItemMutation();
  const [error, setError] = useState<string | null>(null);

  const onAddToSchedule = async () => {
    setError(null);
    try {
      const { errors } = await createScheduleItem({
        variables: {
          input: {
            conferenceId,
            type: "keynote",
            keynoteId: keynote.id,
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
    <Card>
      <Text as="div" weight="bold">
        {keynote.title}
      </Text>
      <InfoRecap
        info={[
          { label: "Type", value: "Keynote" },
          {
            label: "Speaker",
            value: keynote.speakers.map((s) => s.fullName).join(", "),
          },
        ]}
      />
      <Button type="button" onClick={onAddToSchedule}>
        Add to schedule
      </Button>
      {error && (
        <Callout.Root color="red" size="1" mt="2">
          <Callout.Text>{error}</Callout.Text>
        </Callout.Root>
      )}
    </Card>
  );
};
