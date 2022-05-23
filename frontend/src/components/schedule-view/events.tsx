/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, Flex, jsx, Text } from "theme-ui";

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
  if (
    item.type === "submission" ||
    item.type === "training" ||
    item.type === "talk"
  ) {
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

export const ScheduleEntry: React.SFC<{
  adminMode: boolean;
  item: Item;
  slot: Slot;
  rooms: Room[];
  day: string;
}> = ({ item, adminMode, slot, rooms, day, ...props }) => {
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
          height: "100%",
          maxHeight: [null, 135],
          display: "block",
          "> span": {
            height: "100%",
            display: "flex",
            flexDirection: "column",
          },
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
            color:
              item.type === "keynote" || item.type === "talk"
                ? "black"
                : "white",
            mt: ["20px", "auto"],
          }}
        >
          <Box sx={{ mr: "auto" }}>
            <Text sx={{ fontWeight: "bold" }}>
              {item.speakers.map((s) => s.fullName).join(" & ")}
            </Text>
            {audienceLevel && <Text>{audienceLevel}</Text>}
            {item.type === "keynote" && <Text>Keynote</Text>}
            {item.hasLimitedCapacity && item.hasSpacesLeft && (
              <Text sx={{ color: "black" }}>
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
              <Text sx={{ color: "black" }}>
                <FormattedMessage id="talk.eventIsFull" />
              </Text>
            )}
          </Box>

          {(item.type === "submission" ||
            item.type === "training" ||
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
