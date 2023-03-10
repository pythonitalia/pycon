/** @jsxRuntime classic */

/** @jsx jsx */
import {
  Heading,
  Separator,
  ScheduleItemCard,
  Spacer,
  Text,
  Link,
  AvatarGroup,
  Avatar,
  HorizontalStack,
  LayoutContent,
} from "@python-italia/pycon-styleguide";
import { Color } from "@python-italia/pycon-styleguide/dist/types";
import { HeartIcon } from "@python-italia/pycon-styleguide/icons";
import { addMinutes, parseISO } from "date-fns";
import React from "react";
import { FormattedMessage } from "react-intl";
import { jsx, ThemeUIStyleObject } from "theme-ui";

import { useRouter } from "next/router";

import { getColorForSubmission } from "~/helpers/get-color-for-submission";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import {
  readUserStarredScheduleItemsQueryCache,
  writeUserStarredScheduleItemsQueryCache,
  useStarScheduleItemMutation,
  useUnstarScheduleItemMutation,
} from "~/types";

import { createHref } from "../link";
import { useLoginState } from "../profile/hooks";
import { EventTag } from "../schedule-event-detail/event-tag";
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
  className?: string;
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
    <div
      ref={adminMode ? drag : null}
      style={{
        cursor: adminMode ? "move" : "",
      }}
      {...props}
    >
      {children}
    </div>
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
  if (
    item.type === "training" ||
    item.type === "talk" ||
    item.type === "panel"
  ) {
    return `/event/[slug]`;
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
  starred,
  ...props
}: {
  adminMode: boolean;
  item: Item;
  slot: Slot;
  rooms: Room[];
  day: string;
  style?: CSSStyleDeclaration;
  sx?: any;
  starred: boolean;
}) => {
  const router = useRouter();
  const [isLoggedIn] = useLoginState();
  const type = getType(item.submission);
  const language = useCurrentLanguage();
  const [starScheduleItem] = useStarScheduleItemMutation({
    variables: {
      id: item.id,
    },
    optimisticResponse: {
      starScheduleItem: null,
    },
    update(cache) {
      const { me } = readUserStarredScheduleItemsQueryCache({
        cache,
        variables: {
          code: process.env.conferenceCode,
        },
      });
      writeUserStarredScheduleItemsQueryCache({
        cache,
        variables: {
          code: process.env.conferenceCode,
        },
        data: {
          me: {
            ...me,
            starredScheduleItems: [...me.starredScheduleItems, item.id],
          },
        },
      });
    },
  });
  const [unstarScheduleItem] = useUnstarScheduleItemMutation({
    variables: {
      id: item.id,
    },
    optimisticResponse: {
      unstarScheduleItem: null,
    },
    update(cache) {
      const { me } = readUserStarredScheduleItemsQueryCache({
        cache,
        variables: {
          code: process.env.conferenceCode,
        },
      });
      writeUserStarredScheduleItemsQueryCache({
        cache,
        variables: {
          code: process.env.conferenceCode,
        },
        data: {
          me: {
            ...me,
            starredScheduleItems: me.starredScheduleItems.filter(
              (s) => s !== item.id,
            ),
          },
        },
      });
    },
  });

  const toggleEventFavorite = () => {
    if (!isLoggedIn) {
      router.push(`/login?next=/schedule/${day}`);
      return;
    }

    if (!starred) {
      starScheduleItem();
    } else {
      unstarScheduleItem();
    }
  };

  const audienceLevel = item.submission
    ? item.submission.audienceLevel!.name
    : item.audienceLevel
    ? item.audienceLevel.name
    : null;

  const itemUrl = getItemUrl(item);
  const wrapperProps: { hoverColor: Color; href: string } | undefined = itemUrl
    ? {
        hoverColor: "coral",
        href: createHref({
          path: itemUrl,
          locale: language,
          params: {
            slug: item.slug,
          },
        }),
      }
    : undefined;

  const WrapperComponent = itemUrl ? Link : "div";
  const languageText = useTranslatedMessage(
    item.language.code === "en" ? `talk.language.en` : `talk.language.it`,
  );
  const isCustomItem = item.type === "custom";
  const speakersNames = item.speakers.map((s) => s.fullName).join(", ");
  const allRoomsText = useTranslatedMessage("scheduleView.allRooms");

  const roomText =
    item.rooms.length === rooms.length ||
    item.rooms.length ===
      rooms.filter((room) => room.type !== "training").length
      ? allRoomsText
      : item.rooms.map((room) => room.name).join(", ");

  const startHour = parseISO(`${day}T${slot.hour}`);

  const hourFormatter = new Intl.DateTimeFormat(language, {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });

  return (
    <BaseDraggable
      adminMode={adminMode}
      type={type}
      metadata={{ itemId: item.id }}
      className="relative z-20 border-r border-l md:border-0"
      {...props}
    >
      <ScheduleItemCard
        size={slot.type === "FREE_TIME" ? "small" : "large"}
        background={getItemBg(item.type)}
      >
        <div className="flex flex-col md:max-h-[352px] md:h-full justify-between">
          {!isCustomItem && (
            <LayoutContent showUntil="tablet">
              <HorizontalStack
                wrap="wrap"
                gap="medium"
                justifyContent="spaceBetween"
              >
                {speakersNames.length > 0 && (
                  <Heading size={6}>{speakersNames}</Heading>
                )}
                <Text size="label4" color="grey-700">
                  {[roomText, audienceLevel, languageText]
                    .filter((v) => v)
                    .join(", ")}
                </Text>
              </HorizontalStack>
              <Spacer size="small" />
            </LayoutContent>
          )}

          <div className="flex flex-col-reverse items-start md:flex-col gap-6 md:gap-2">
            {!isCustomItem && (
              <div className="w-full">
                {item.hasLimitedCapacity && (
                  <LayoutContent showUntil="tablet">
                    <Text as="p" size="label3" color="grey-700">
                      {item.spacesLeft > 0 && (
                        <FormattedMessage id="schedule.workshop.limitedSeats" />
                      )}
                      {item.spacesLeft <= 0 && (
                        <FormattedMessage id="schedule.workshop.soldout" />
                      )}
                    </Text>
                    <Spacer size="small" />
                  </LayoutContent>
                )}
                <HorizontalStack
                  fullWidth
                  alignItems="center"
                  justifyContent="spaceBetween"
                  gap="small"
                  wrap="wrap"
                >
                  <EventTag type={item.type} />
                  <HeartIcon filled={starred} onClick={toggleEventFavorite} />
                </HorizontalStack>
              </div>
            )}

            <WrapperComponent {...wrapperProps}>
              <Heading color="none" size={4}>
                {item.title}
              </Heading>
              {item.duration && (
                <>
                  <Spacer size="thin" />
                  <Text size="label3" color="grey-700">
                    <FormattedMessage
                      id="schedule.entry.endsAt"
                      values={{
                        time: (
                          <Text weight="strong" size="label3">
                            {hourFormatter.format(
                              addMinutes(startHour, item.duration),
                            )}
                          </Text>
                        ),
                      }}
                    />
                  </Text>
                </>
              )}
            </WrapperComponent>
          </div>

          {!isCustomItem && (
            <LayoutContent showFrom="tablet">
              <div>
                {item.hasLimitedCapacity && (
                  <Text as="p" size="label3" color="grey-700">
                    {item.spacesLeft > 0 && (
                      <FormattedMessage id="schedule.workshop.limitedSeats" />
                    )}
                    {item.spacesLeft <= 0 && (
                      <FormattedMessage id="schedule.workshop.soldout" />
                    )}
                  </Text>
                )}

                <Text size="label3" color="grey-500">
                  {[audienceLevel, languageText].filter((v) => v).join(", ")}
                </Text>
              </div>
              {item.speakers.length > 0 && (
                <>
                  <Spacer size="small" />
                  <Separator />
                  <Spacer size="small" />
                  <HorizontalStack
                    alignItems="center"
                    justifyContent="spaceBetween"
                    gap="small"
                  >
                    <Heading size={5}>{speakersNames}</Heading>
                    <AvatarGroup>
                      {item.speakers.map((speaker) => (
                        <Avatar
                          image={speaker.participant?.photo}
                          letter={speaker.fullName}
                          letterBackgroundColor={getAvatarBackgroundColor(
                            parseInt(item.id, 10),
                          )}
                        />
                      ))}
                    </AvatarGroup>
                  </HorizontalStack>
                </>
              )}
            </LayoutContent>
          )}
        </div>
      </ScheduleItemCard>
    </BaseDraggable>
  );
};

const getItemBg = (type: string) => {
  if (type === "custom") {
    return "milk";
  }

  return "cream";
};

const BACKGROUND_COLORS: Color[] = [
  "coral",
  "caramel",
  "yellow",
  "green",
  "blue",
  "purple",
  "pink",
  "red",
];
const getAvatarBackgroundColor = (index: number): Color => {
  return BACKGROUND_COLORS[Math.floor(index % BACKGROUND_COLORS.length)];
};
