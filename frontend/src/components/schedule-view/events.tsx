/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, Flex, jsx, Text, ThemeUIStyleObject } from "theme-ui";

import { EnglishIcon } from "~/components/icons/english";
import { ItalianIcon } from "~/components/icons/italian";
import { Link } from "~/components/link";
import {
  getColorForItem,
  getColorForSubmission,
} from "~/helpers/get-color-for-submission";

import {
  Item,
  ItemTypes,
  Room,
  Slot,
  Submission as SubmissionType,
} from "./types";
import { useDragOrDummy } from "./use-drag-or-dummy";

const getType = (submission?: SubmissionType | null) =>
  submission?.type?.name.toLowerCase() === "tutorial"
    ? ItemTypes.TRAINING
    : ItemTypes.TALK;

const BaseDraggable = ({
  adminMode,
  type,
  children,
  metadata,
  ...props
}: {
  type: string;
  metadata?: any;
  adminMode?: boolean;
  sx?: ThemeUIStyleObject;
  children: any;
}) => {
  const [_, drag] = useDragOrDummy({
    adminMode,
    item: {
      type,
      ...metadata,
    },
    collect: (monitor) => ({
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

export const BaseEvent = ({
  type,
  children,
  metadata,
  ...props
}: {
  type: string;
  metadata: any;
  sx?: ThemeUIStyleObject;
  children: any;
}) => (
  <BaseDraggable
    type={type}
    adminMode={true}
    metadata={metadata}
    sx={{
      display: "inline-block",
      border: "primary",
      p: 3,
      mb: "-4px",
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
  sx?: any;
}) => {
  const itemType = getType(submission);

  return (
    <BaseEvent
      type={itemType}
      metadata={{ event: { submissionId: submission.id } }}
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

export const getItemUrl = (item: Item) => {
  if (item.type === "training" || item.type === "talk") {
    return `/talk/[slug]`;
  }

  if (item.type === "keynote") {
    return `/keynotes/[slug]`;
  }

  return undefined;
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

export const RoomChangeEvent = ({ ...props }) => (
  <BaseEvent
    type={ItemTypes.ALL_TRACKS_EVENT}
    metadata={{ event: { roomChange: true } }}
    {...props}
  >
    Room change event
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

export const Keynote = ({ keynote, ...props }) => (
  <BaseEvent
    type={ItemTypes.KEYNOTE}
    metadata={{ event: { keynoteId: keynote.id } }}
    sx={{
      backgroundColor: "yellow",
    }}
    {...props}
  >
    {keynote.title}
  </BaseEvent>
);

export const ScheduleEntry = ({
  item,
  adminMode,
  slot,
  rooms,
  day,
  ...props
}: {
  adminMode: boolean;
  item: Item;
  slot: Slot;
  rooms: Room[];
  day: string;
  sx?: any;
}) => {
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

  const itemUrl = getItemUrl(item);
  const WrapperComponent = itemUrl ? Link : Box;

  return (
    <BaseDraggable
      adminMode={adminMode}
      type={type}
      metadata={{ itemId: item.id }}
      sx={{
        zIndex: ["scheduleDraggable"],
        backgroundColor,
        position: "relative",
        px: [20, 2],
        py: [3, 2],
        fontSize: 1,
      }}
      {...props}
    >
      <WrapperComponent
        path={itemUrl}
        params={{ slug: item.slug, day }}
        sx={{
          color: "inherit",
          textDecoration: "none",
          maxHeight: [null, 135],
          height: "100%",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Text>
          {item.type !== "custom" ? (
            <Text
              sx={{
                fontWeight: "bold",
                display: ["block", "none"],
                mb: 2,
              }}
            >
              {item.rooms.map((room) => room.name).join(", ")}
            </Text>
          ) : null}

          {item.title}

          {marker && (
            <Text as="span" sx={{ fontWeight: "bold" }}>
              {" "}
              {marker}
            </Text>
          )}
        </Text>

        <Flex
          sx={{
            color: !audienceLevel ? "black" : "white",
            mt: ["20px", "auto"],
          }}
        >
          <Box sx={{ mr: "auto" }}>
            <Text sx={{ fontWeight: "bold", display: "block" }}>
              {item.speakers.map((s) => s.fullName).join(" & ")}
            </Text>
            {audienceLevel && <Text>{audienceLevel}</Text>}
            {item.type === "keynote" && <Text>Keynote</Text>}
            {item.hasLimitedCapacity && item.hasSpacesLeft && (
              <Text sx={{ color: "black", display: "block" }}>
                <FormattedMessage
                  id="talk.spacesLeft"
                  values={{
                    spacesLeft: (
                      <Text as="span" sx={{ fontWeight: "bold" }}>
                        {item.spacesLeft}
                      </Text>
                    ),
                  }}
                />
              </Text>
            )}
            {item.hasLimitedCapacity && !item.hasSpacesLeft && (
              <Text sx={{ color: "black", display: "block" }}>
                <FormattedMessage id="talk.eventIsFull" />
              </Text>
            )}
          </Box>

          {(item.type === "training" ||
            item.type === "keynote" ||
            item.type === "talk") && (
            <LanguageIcon
              sx={{
                width: 30,
                flexShrink: 0,
              }}
            />
          )}
        </Flex>
      </WrapperComponent>
    </BaseDraggable>
  );
};
