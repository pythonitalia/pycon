import {
  Container,
  Heading,
  Link,
  ScheduleItemCard,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { Color } from "@python-italia/pycon-styleguide/dist/types";
import { HeartIcon } from "@python-italia/pycon-styleguide/icons";
import clsx from "clsx";
import { addMinutes, parseISO } from "date-fns";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";

import { isItemVisible } from ".";
import { createHref } from "../link";
import { EventTag } from "../schedule-event-detail/event-tag";
import { getItemBg, getItemUrl } from "./events";
import { Item, Slot, Room } from "./types";

type Props = {
  slots: Slot[];
  currentDay: string;
  rooms: Room[];
  toggleEventFavorite: (item: Item) => void;
  starredScheduleItems: string[];
  currentFilters: Record<string, string[]>;
  liveSlot: Slot | null;
};

export const ScheduleList = ({
  slots,
  rooms,
  currentDay,
  toggleEventFavorite,
  currentFilters,
  starredScheduleItems,
  liveSlot,
}: Props) => {
  return (
    <Container>
      <div className="divide-y border-x border-y">
        {slots.map((slot) => {
          const startHour = parseISO(`${currentDay}T${slot.hour}`);
          const isLive = liveSlot?.id === slot.id;

          return slot.items.map((item) => {
            const starred = starredScheduleItems.includes(item.id);
            const filteredOut = !isItemVisible(item, currentFilters, starred);

            if (filteredOut) {
              return null;
            }

            return (
              <ScheduleItem
                item={item}
                currentDay={currentDay}
                slot={slot}
                isLive={isLive}
                startHour={startHour}
                starred={starred}
                toggleEventFavorite={toggleEventFavorite}
                rooms={rooms}
              />
            );
          });
        })}
      </div>
    </Container>
  );
};

const ScheduleItem = ({
  item,
  slot,
  isLive,
  startHour,
  starred,
  rooms,
  toggleEventFavorite,
  currentDay,
}: {
  item: Item;
  slot: Slot;
  isLive: boolean;
  startHour: Date;
  starred: boolean;
  rooms: Room[];
  toggleEventFavorite: (item: Item) => void;
  currentDay: string;
}) => {
  const language = useCurrentLanguage();
  const italianLanguageText = useTranslatedMessage(`talk.language.it`);
  const englishLanguageText = useTranslatedMessage(`talk.language.en`);
  const allRoomsText = useTranslatedMessage("scheduleView.allRooms");
  const translatedRoomText = useTranslatedMessage("schedule.room");

  const hourFormatter = new Intl.DateTimeFormat(language, {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });

  const endHour = item.duration
    ? addMinutes(startHour, item.duration)
    : parseISO(`${currentDay}T${slot.endHour}`);

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

  const roomText =
    item.type === "keynote" ||
    item.rooms.length === rooms.length ||
    item.rooms.length ===
      rooms.filter((room) => room.type !== "training").length
      ? allRoomsText
      : `${translatedRoomText} ${item.rooms
          .map((room) => room.name)
          .join(`, ${translatedRoomText} `)}`;

  const info = [
    item.audienceLevel?.name ?? item.submission?.audienceLevel?.name,
    item.language.code === "it" ? italianLanguageText : englishLanguageText,
  ]
    .filter((t) => t)
    .join(", ");

  const isBreak = item.type === "break" || item.type === "custom";

  return (
    <div
      className="grid md:grid-cols-[100px_1fr] lg:grid-cols-[130px_1fr] divide-x"
      key={item.id}
    >
      <div
        className={clsx("flex items-center justify-center flex-col gap-1", {
          "bg-coral": isLive,
        })}
      >
        <Heading size={6}>
          {isBreak && (
            <FormattedMessage
              id="schedule.timeNoEnd"
              values={{
                start: hourFormatter.format(startHour),
              }}
            />
          )}
          {!isBreak && (
            <FormattedMessage
              id="schedule.time"
              values={{
                start: hourFormatter.format(startHour),
                end: hourFormatter.format(endHour),
              }}
            />
          )}
        </Heading>
        {isLive && (
          <Text as="p" size="label4" uppercase weight="strong">
            <FormattedMessage id="schedule.live" />
          </Text>
        )}
      </div>
      <ScheduleItemCard background={getItemBg(item.type)} size="large">
        <div className="flex justify-between transition-opacity">
          <div>
            {!isBreak && (
              <>
                <div className="flex flex-row items-center md:gap-3 lg:gap-6">
                  {item.speakers.length > 0 && (
                    <Heading size={6}>
                      {item.speakers
                        .map((speaker) => speaker.fullName)
                        .join(", ")}
                    </Heading>
                  )}
                  <Text size={3} color="grey-500">
                    {info}
                  </Text>
                </div>
                <Spacer size="xs" />
              </>
            )}
            <WrapperComponent {...wrapperProps}>
              <div className="max-w-[580px] w-full">
                <Heading color="none" size={4}>
                  {item.title}
                </Heading>
              </div>
            </WrapperComponent>
          </div>
          {!isBreak && (
            <div className="flex flex-col gap-1">
              <div className="flex items-center justify-end gap-3">
                <HeartIcon
                  filled={starred}
                  onClick={() => toggleEventFavorite(item)}
                />
                <EventTag type={item.type} />
              </div>

              {item.hasLimitedCapacity && (
                <Text as="p" size={3} color="grey-700" align="right">
                  {item.spacesLeft > 0 && (
                    <FormattedMessage id="schedule.workshop.limitedSeats" />
                  )}
                  {item.spacesLeft <= 0 && (
                    <FormattedMessage id="schedule.workshop.soldout" />
                  )}
                </Text>
              )}
              <Text as="p" size={3} color="grey-700" align="right">
                {roomText}
              </Text>
            </div>
          )}
        </div>
      </ScheduleItemCard>
    </div>
  );
};
