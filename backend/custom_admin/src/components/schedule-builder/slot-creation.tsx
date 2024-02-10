import { useCurrentConference } from "../utils/conference";
import { useCreateScheduleSlotMutation } from "./create-schedule-slot.generated";

export const SlotCreation = ({ dayId }) => {
  return (
    <div className="grid grid-cols-4 gap-3 mt-3">
      <AddSlotButton dayId={dayId} type="default" duration={15}>
        Add 15 mins slot
      </AddSlotButton>
      <AddSlotButton dayId={dayId} type="default" duration={30}>
        Add 30 mins slot
      </AddSlotButton>
      <AddSlotButton dayId={dayId} type="default" duration={45}>
        Add 45 mins slot
      </AddSlotButton>
      <AddSlotButton dayId={dayId} type="default" duration={60}>
        Add 60 mins slot
      </AddSlotButton>
      <AddSlotButton dayId={dayId} type="break" duration={10}>
        Break slot: Add 10 mins slot
      </AddSlotButton>
      <AddSlotButton dayId={dayId} type="break" duration={125}>
        Lunch slot: 2h 5 mins
      </AddSlotButton>
      <AddSlotButton dayId={dayId} type="break" duration={30}>
        Break slot: 30 mins
      </AddSlotButton>
    </div>
  );
};

const AddSlotButton = ({ children, duration, type, dayId }) => {
  const conferenceId = useCurrentConference();
  const [createScheduleSlot] = useCreateScheduleSlotMutation();

  const onCreateSlot = (e) => {
    e.preventDefault();
    createScheduleSlot({
      variables: {
        input: {
          conferenceId,
          duration,
          type,
          dayId,
        },
      },
    });
  };

  return (
    <button className="btn" onClick={onCreateSlot}>
      {children}
    </button>
  );
};
