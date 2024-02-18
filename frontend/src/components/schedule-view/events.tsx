/** @jsxRuntime classic */

/** @jsx jsx */
import {
  Avatar,
  AvatarGroup,
  Heading,
  HorizontalStack,
  LayoutContent,
  Link,
  ScheduleItemCard,
  Separator,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { Color } from "@python-italia/pycon-styleguide/dist/types";
import { HeartIcon } from "@python-italia/pycon-styleguide/icons";
import clsx from "clsx";
import { addMinutes, parseISO } from "date-fns";
import React from "react";
import { FormattedMessage } from "react-intl";
import { ThemeUIStyleObject, jsx } from "theme-ui";

import { useRouter } from "next/router";

import { getColorForSubmission } from "~/helpers/get-color-for-submission";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import {
  readUserStarredScheduleItemsQueryCache,
  useStarScheduleItemMutation,
  useUnstarScheduleItemMutation,
  writeUserStarredScheduleItemsQueryCache,
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

export const getItemUrl = (item: Item) => {
  if (
    item.type === "training" ||
    item.type === "talk" ||
    item.type === "panel" ||
    item.type === "social" ||
    item.type === "announcements" ||
    item.type === "registration"
  ) {
    return "/event/[slug]";
  }

  if (item.type === "keynote") {
    return "/keynotes/[slug]";
  }

  return undefined;
};

export const ScheduleEntry = ({
  item,
  slot,
  rooms,
  day,
  starred,
  filteredOut,
  toggleEventFavorite,
  sameSlotItem,
  ...props
}: {
  item: Item;
  slot: Slot;
  rooms: Room[];
  day: string;
  style?: CSSStyleDeclaration;
  sx?: any;
  starred: boolean;
  filteredOut: boolean;
  sameSlotItem: boolean;
  toggleEventFavorite: (item: Item) => void;
}) => {
  const language = useCurrentLanguage();

  const audienceLevel = item.submission
    ? item.submission.audienceLevel!.name
    : item.audienceLevel
      ? item.audienceLevel.name
      : null;
  const duration =
    item.duration || slot.duration || item.submission?.duration?.duration;

  const itemUrl = getItemUrl(item);
  const wrapperProps: any = itemUrl
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
  const durationText = `${duration} min`;
  const languageText = useTranslatedMessage(
    item.language.code === "en" ? "talk.language.en" : "talk.language.it",
  );
  const isCustomItem = item.type === "custom" || item.type === "break";
  const speakersNames = item.speakers.map((s) => s.fullName).join(", ");
  const allRoomsText = useTranslatedMessage("scheduleView.allRooms");

  const roomText =
    item.type === "keynote" ||
    item.rooms.length === rooms.length ||
    item.rooms.length ===
      rooms.filter((room) => room.type !== "training").length
      ? allRoomsText
      : `Room ${item.rooms.map((room) => room.name).join(", Room ")}`;

  const startHour = parseISO(`${day}T${slot.hour}`);

  const hourFormatter = new Intl.DateTimeFormat(language, {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });

  return (
    <div
      className={clsx("relative z-20 border-r border-l md:border-0", {
        "hidden md:block": filteredOut,
        "md:!border-b-3 md:border-b-black md:!border-0 md:!border-solid":
          sameSlotItem,
      })}
      {...(props as any)}
    >
      <ScheduleItemCard
        size={["FREE_TIME", "BREAK"].includes(slot.type) ? "small" : "large"}
        background={getItemBg(item.type)}
      >
        <div
          className={clsx(
            "flex flex-col md:max-h-[352px] md:h-full justify-between transition-opacity",
            {
              "md:flex md:opacity-20": filteredOut,
            },
          )}
        >
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
                <Text size="label4">
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
                  <HeartIcon
                    filled={starred}
                    onClick={(_) => toggleEventFavorite(item)}
                  />
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
                  {[durationText, audienceLevel, languageText]
                    .filter((v) => v)
                    .join(", ")}
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
                          key={speaker.fullName}
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
    </div>
  );
};

export const getItemBg = (type: string) => {
  if (type === "custom" || type === "break") {
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
