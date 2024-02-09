import { useCurrentConference } from "../../utils/conference";
import { useAddItemModal } from "./context";
import { useCreateScheduleItemMutation } from "./create-schedule-item.generated";

export const AddCustomEvent = () => {
  const { data } = useAddItemModal();
  const conferenceId = useCurrentConference();
  const [createScheduleItem] = useCreateScheduleItemMutation();

  const onCreate = async ({ title, type }: { title: string; type: string }) => {
    await createScheduleItem({
      variables: {
        input: {
          conferenceId,
          type: type,
          title: title,
          slotId: data.slot.id,
          rooms: [data.room.id],
          languageId: null,
        },
      },
    });
  };

  return (
    <div>
      <strong>Add Custom from list:</strong>
      <ul className="my-2">
        <Option onClick={onCreate} type="break">
          Room change
        </Option>
        <Option onClick={onCreate} type="break">
          Lunch 🍝
        </Option>
        <Option onClick={onCreate} type="break">
          Coffee Break ☕️
        </Option>
        <Option onClick={onCreate} type="break">
          Welcome Coffee
        </Option>
        <Option onClick={onCreate} type="custom">
          Keynote TBA
        </Option>
        <Option onClick={onCreate} type="announcements">
          Opening
        </Option>
        <Option onClick={onCreate} type="registration">
          Registration
        </Option>
        <Option onClick={onCreate} type="announcements">
          Closing
        </Option>
      </ul>

      <strong>Create custom by hand:</strong>
      <div className="my-2 grid gap-2 grid-cols-[50px_1fr] items-center">
        <label htmlFor="title">
          <strong>Title</strong>
        </label>
        <input id="title" className="p-2 border" type="text" />
        <label htmlFor="type">
          <strong>Type</strong>
        </label>
        <select id="type" className="p-2 border">
          <option value="talk">Talk</option>
          <option value="training">Training</option>
          <option value="keynote">Keynote</option>
          <option value="panel">Panel</option>
          <option value="registration">Registration</option>
          <option value="announcements">Announcements</option>
          <option value="break">Break</option>
          <option value="custom">Custom</option>
        </select>
      </div>
      <button className="btn w-full">Create</button>
    </div>
  );
};

const Option = ({ children, type, onClick }) => {
  return (
    <li
      onClick={() => {
        onClick({
          title: children,
          type: type,
        });
      }}
      className="p-2 bg-slate-300 odd:bg-slate-200 cursor-pointer hover:bg-slate-400"
    >
      {children}
    </li>
  );
};
