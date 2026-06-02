import { Button, Card, Text } from "@radix-ui/themes";
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

  const onAddToSchedule = async () => {
    await createScheduleItem({
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
    close();
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
    </Card>
  );
};
