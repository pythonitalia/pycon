import type { Keynote } from "../../../types";
import { useCurrentConference } from "../../utils/conference";
import { useAddItemModal } from "./context";
import { useCreateScheduleItemMutation } from "./create-schedule-item.generated";
import { InfoRecap } from "./info-recap";

export const KeynotePreview = ({ keynote }: { keynote: Keynote }) => {
  const conferenceId = useCurrentConference();
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
    <li className="p-2 bg-slate-300 odd:bg-slate-200">
      <strong>{keynote.title}</strong>
      <InfoRecap
        info={[
          { label: "Type", value: `Keynote` },
          { label: "Speaker", value: keynote.name },
        ]}
      />
      <button onClick={onAddToSchedule} className="btn">
        Add to schedule
      </button>
    </li>
  );
};
