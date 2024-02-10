import { useState } from "react";

import type { Room } from "../../../types";
import { useCurrentConference } from "../../utils/conference";
import { useAddItemModal } from "./context";
import { useCreateScheduleItemMutation } from "./create-schedule-item.generated";

export const AddCustomEvent = () => {
  const { data, close } = useAddItemModal();
  const conferenceId = useCurrentConference();
  const [createScheduleItem] = useCreateScheduleItemMutation();

  const onCreate = async ({
    title,
    type,
    rooms,
  }: {
    title: string;
    type: string;
    rooms: Room[];
  }) => {
    await createScheduleItem({
      variables: {
        input: {
          conferenceId,
          type: type,
          title: title,
          slotId: data.slot.id,
          rooms: rooms.map((room) => room.id),
          languageId: null,
        },
      },
    });
    close();
  };

  return (
    <div>
      <CustomDefinedOptions onCreate={onCreate} />
      <CustomByHand onCreate={onCreate} />
    </div>
  );
};

const CustomDefinedOptions = ({ onCreate }) => {
  const {
    data: {
      day: { rooms },
    },
  } = useAddItemModal();
  const allTalkRooms = rooms.filter((room) => room.type === "talk");
  const allRooms = rooms;

  return (
    <>
      <strong>Add Custom from list</strong>
      <ul className="my-2">
        <Option onClick={onCreate} type="break" rooms={allTalkRooms}>
          Room change
        </Option>
        <Option onClick={onCreate} type="break" rooms={allRooms}>
          Lunch 🍝
        </Option>
        <Option onClick={onCreate} type="break" rooms={allRooms}>
          Coffee Break ☕️
        </Option>
        <Option onClick={onCreate} type="break" rooms={allRooms}>
          Welcome Coffee
        </Option>
        <Option onClick={onCreate} type="custom" rooms={allRooms}>
          Keynote Announcement Soon!
        </Option>
        <Option onClick={onCreate} type="announcements" rooms={allTalkRooms}>
          Opening
        </Option>
        <Option onClick={onCreate} type="registration" rooms={allTalkRooms}>
          Registration
        </Option>
        <Option onClick={onCreate} type="announcements" rooms={allRooms}>
          Closing
        </Option>
      </ul>
    </>
  );
};

const Option = ({ children, type, rooms, onClick }) => {
  return (
    <li
      onClick={() => {
        onClick({
          title: children,
          type,
          rooms,
        });
      }}
      className="p-2 bg-slate-300 odd:bg-slate-200 cursor-pointer hover:bg-slate-400"
    >
      {children}
    </li>
  );
};

const CustomByHand = ({ onCreate }) => {
  const {
    data: { room: selectedRoom },
  } = useAddItemModal();

  const [title, setTitle] = useState("");
  const [type, setType] = useState("");

  const create = () => {
    if (!title || type === "") {
      return;
    }
    onCreate({ title, type, rooms: [selectedRoom] });
  };

  return (
    <>
      <strong>Create custom by hand</strong>
      <div className="my-2 grid gap-2 grid-cols-[50px_1fr] items-center">
        <label htmlFor="title">
          <strong>Title</strong>
        </label>
        <input
          id="title"
          className="p-2 border"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <label htmlFor="type">
          <strong>Type</strong>
        </label>
        <select
          id="type"
          className="p-2 border"
          value={type}
          onChange={(e) => setType(e.target.selectedOptions[0].value)}
        >
          <option value="" disabled>
            Choose one
          </option>
          <option value="talk">Talk</option>
          <option value="training">Training</option>
          <option value="keynote">Keynote</option>
          <option value="panel">Panel</option>
          <option value="registration">Registration</option>
          <option value="announcements">Announcements</option>
          <option value="break">Break</option>
          <option value="social">Social</option>
          <option value="custom">Custom</option>
        </select>
      </div>
      <button
        disabled={!title || type === ""}
        onClick={create}
        className="btn w-full mt-3"
      >
        Create
      </button>
    </>
  );
};
