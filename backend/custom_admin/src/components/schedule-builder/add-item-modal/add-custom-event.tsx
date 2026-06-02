import {
  Button,
  Callout,
  Flex,
  Heading,
  Select,
  Text,
  TextField,
} from "@radix-ui/themes";
import { useState } from "react";

import type { Room } from "../../../types";
import { useCurrentConference } from "../../utils/conference";
import { useAddItemModal } from "./context";
import { useCreateScheduleItemMutation } from "./create-schedule-item.generated";

type CreateArgs = { title: string; type: string; rooms: Room[] };

export const AddCustomEvent = () => {
  const { data, close } = useAddItemModal();
  const { conferenceId } = useCurrentConference();
  const [createScheduleItem] = useCreateScheduleItemMutation();
  const [error, setError] = useState<string | null>(null);

  const onCreate = async ({ title, type, rooms }: CreateArgs) => {
    setError(null);
    try {
      const { errors } = await createScheduleItem({
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
    <Flex direction="column" gap="4">
      {error && (
        <Callout.Root color="red" size="1">
          <Callout.Text>{error}</Callout.Text>
        </Callout.Root>
      )}
      <CustomDefinedOptions onCreate={onCreate} />
      <CustomByHand onCreate={onCreate} />
    </Flex>
  );
};

const CustomDefinedOptions = ({
  onCreate,
}: {
  onCreate: (args: CreateArgs) => void;
}) => {
  const {
    data: {
      day: { rooms },
    },
  } = useAddItemModal();
  const allTalkRooms = rooms.filter((room) => room.type === "talk");
  const allRooms = rooms;

  return (
    <Flex direction="column" gap="2">
      <Heading size="3">Add custom from list</Heading>
      <Flex direction="column" gap="1">
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
        <Option onClick={onCreate} type="announcements" rooms={allRooms}>
          Opening
        </Option>
        <Option onClick={onCreate} type="registration" rooms={allRooms}>
          Registration
        </Option>
        <Option onClick={onCreate} type="announcements" rooms={allRooms}>
          Closing
        </Option>
      </Flex>
    </Flex>
  );
};

const Option = ({
  children,
  type,
  rooms,
  onClick,
}: {
  children: string;
  type: string;
  rooms: Room[];
  onClick: (args: CreateArgs) => void;
}) => {
  return (
    <Button
      variant="soft"
      color="gray"
      style={{ justifyContent: "flex-start" }}
      onClick={() => onClick({ title: children, type, rooms })}
    >
      {children}
    </Button>
  );
};

const TYPE_OPTIONS = [
  { value: "talk", label: "Talk" },
  { value: "training", label: "Training" },
  { value: "keynote", label: "Keynote" },
  { value: "panel", label: "Panel" },
  { value: "registration", label: "Registration" },
  { value: "announcements", label: "Announcements" },
  { value: "break", label: "Break" },
  { value: "social", label: "Social" },
  { value: "recruiting", label: "Recruiting" },
  { value: "custom", label: "Custom" },
];

const CustomByHand = ({
  onCreate,
}: {
  onCreate: (args: CreateArgs) => void;
}) => {
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
    <Flex direction="column" gap="2">
      <Heading size="3">Create custom by hand</Heading>
      <Flex align="center" gap="3">
        <Text weight="bold" style={{ width: 50 }}>
          Title
        </Text>
        <TextField.Root
          style={{ flex: 1 }}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </Flex>
      <Flex align="center" gap="3">
        <Text weight="bold" style={{ width: 50 }}>
          Type
        </Text>
        <Select.Root value={type || undefined} onValueChange={setType}>
          <Select.Trigger placeholder="Choose one" />
          <Select.Content position="popper">
            {TYPE_OPTIONS.map((option) => (
              <Select.Item key={option.value} value={option.value}>
                {option.label}
              </Select.Item>
            ))}
          </Select.Content>
        </Select.Root>
      </Flex>
      <Button
        type="button"
        disabled={!title || type === ""}
        onClick={create}
        mt="2"
      >
        Create
      </Button>
    </Flex>
  );
};
