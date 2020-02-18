/** @jsx jsx */
import { Box, Flex, Text } from "@theme-ui/components";
import React from "react";
import { useDrag } from "react-dnd";
import { jsx } from "theme-ui";

import { EnglishIcon } from "../../components/icons/english";
import { ItalianIcon } from "../../components/icons/italian";
import { Link } from "../../components/link";
import { getColorForItem, getColorForSubmission } from "./get-color";
import {
  Item,
  ItemTypes,
  Room,
  Slot,
  Submission as SubmissionType,
} from "./types";
import { useDragOrDummy } from "./useDragOrDummy";

const getType = (submission?: SubmissionType | null) =>
  submission?.type?.name.toLowerCase() === "tutorial"
    ? ItemTypes.TRAINING
    : ItemTypes.TALK;

const BaseDraggable: React.SFC<{
  type: string;
  metadata?: any;
  adminMode?: boolean;
}> = ({ adminMode, type, children, metadata, ...props }) => {
  const [_, drag] = useDragOrDummy({
    adminMode,
    item: {
      type,
      ...metadata,
    },
    collect: monitor => ({
      isDragging: !!monitor.isDragging(),
    }),
  });

  return (
    <Box
      ref={adminMode ? drag : null}
      sx={{
        cursor: adminMode ? "move" : "",
      }}
      {...props}
    >
      {children}
    </Box>
  );
};

export const BaseEvent: React.SFC<{ type: string; metadata: any }> = ({
  type,
  children,
  metadata,
  ...props
}) => (
  <BaseDraggable
    type={type}
    adminMode={true}
    metadata={metadata}
    sx={{
      display: "inline-block",
      border: "primary",
      p: 3,
      mb: "-3px",
      mr: 3,
    }}
    {...props}
  >
    {children}
  </BaseDraggable>
);

export const Submission = ({
  submission,
  ...props
}: {
  submission: SubmissionType;
}) => {
  const itemType = getType(submission);

  return (
    <BaseEvent
      type={itemType}
      metadata={{ event: { id: submission.id } }}
      sx={{ backgroundColor: getColorForSubmission(submission) }}
      {...props}
    >
      {submission.title}{" "}
      <Text as="span" sx={{ fontWeight: "bold" }}>
        ({submission.duration!.duration} minutes)
      </Text>
      <Text sx={{ fontWeight: "bold", color: "white", mt: 2 }}>
        {submission.speaker?.fullName || "No name"}
      </Text>
    </BaseEvent>
  );
};

const getItemUrl = (item: Item) => {
  if (item.type === "submission") {
    return `/:language/talk/${item.slug}`;
  }

  // TODO: check tbd
  if (item.type === "keynote") {
    return `/:language/keynote/${item.slug}`;
  }

  return null;
};

export const AllTracksEvent = ({ ...props }) => (
  <BaseEvent
    type={ItemTypes.ALL_TRACKS_EVENT}
    metadata={{ event: { allTracks: true } }}
    {...props}
  >
    All track event
  </BaseEvent>
);

export const CustomEvent = ({ ...props }) => (
  <BaseEvent
    type={ItemTypes.CUSTOM}
    metadata={{ event: { title: "Custom" } }}
    {...props}
  >
    Custom event
  </BaseEvent>
);

export const ScheduleEntry: React.SFC<{
  adminMode: boolean;
  item: Item;
  slot: Slot;
  rooms: Room[];
}> = ({ item, adminMode, slot, rooms, ...props }) => {
  const type = getType(item.submission);

  const backgroundColor = getColorForItem(item);

  const itemDuration = item.submission
    ? item.submission.duration!.duration
    : slot.duration;

  const marker =
    adminMode && itemDuration !== slot.duration ? `*${itemDuration}` : null;

  const LanguageIcon = item.language.code === "en" ? EnglishIcon : ItalianIcon;

  const audienceLevel = item.submission
    ? item.submission.audienceLevel!.name
    : item.audienceLevel
    ? item.audienceLevel.name
    : null;

  return (
    <BaseDraggable
      adminMode={adminMode}
      type={type}
      metadata={{ itemId: item.id }}
      sx={{
        zIndex: ["scheduleDraggable"],
        backgroundColor,
        position: "relative",
        p: 2,
        fontSize: 1,
      }}
      {...props}
    >
      <Link
        href={getItemUrl(item)}
        sx={{
          color: "inherit",
          textDecoration: "none",
          height: "100%",
          maxHeight: 135,
          display: "block",
          "> span": {
            height: "100%",
            display: "flex",
            flexDirection: "column",
          },
        }}
      >
        <Text>
          {item.title}

          {marker && (
            <Text as="span" sx={{ fontWeight: "bold" }}>
              {" "}
              {marker}
            </Text>
          )}
        </Text>

        <Flex sx={{ color: "white", mt: "auto" }}>
          <Box sx={{ mr: "auto" }}>
            <Text sx={{ fontWeight: "bold" }}>
              {item.speakers.map(s => s.fullName).join(" & ")}
            </Text>
            {audienceLevel && <Text>{audienceLevel}</Text>}
          </Box>

          {item.submission && (
            <LanguageIcon
              sx={{
                width: 30,
              }}
            />
          )}
        </Flex>
      </Link>
    </BaseDraggable>
  );
};
