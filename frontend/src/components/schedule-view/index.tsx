import {
  DaysSelector,
  FilterBar,
  Heading,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import va from "@vercel/analytics";
import { isAfter, isBefore, parseISO } from "date-fns";
import { fromZonedTime } from "date-fns-tz";
import React, {
  Fragment,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import { FormattedMessage } from "react-intl";

import { useRouter } from "next/router";

import { useCurrentLanguage } from "~/locale/context";
import { getDayUrl } from "~/pages/schedule/[day]";
import {
  type ScheduleQuery,
  readUserStarredScheduleItemsQueryCache,
  useStarScheduleItemMutation,
  useUnstarScheduleItemMutation,
  useUserStarredScheduleItemsQuery,
  writeUserStarredScheduleItemsQueryCache,
} from "~/types";

import { useSetCurrentModal } from "../modal/context";
import { useLoginState } from "../profile/hooks";
import { Schedule } from "./schedule";
import { ScheduleList } from "./schedule-list";
import type { Item, Slot } from "./types";

export type ViewMode = "grid" | "list";

export const ScheduleView = ({
  day: currentDay,
  schedule,
  changeDay,
}: {
  day?: string;
  schedule: ScheduleQuery;
  changeDay: (day: string) => void;
}) => {
  const setCurrentModal = useSetCurrentModal();
  const router = useRouter();
  const [isLoggedIn] = useLoginState();
  const language = useCurrentLanguage();
  const [liveSlot, setLiveSlot] = useState<Slot | null>(null);

  const {
    data: {
      me: { starredScheduleItems = [] } = {},
    } = {},
  } = useUserStarredScheduleItemsQuery({
    skip: !isLoggedIn,
    variables: {
      code: process.env.conferenceCode,
    },
  });

  const [starScheduleItem] = useStarScheduleItemMutation({
    optimisticResponse: {
      starScheduleItem: { ok: true },
    },
    update(cache, _, { variables }) {
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
            starredScheduleItems: [...me.starredScheduleItems, variables.id],
          },
        },
      });
    },
  });
  const [unstarScheduleItem] = useUnstarScheduleItemMutation({
    optimisticResponse: {
      unstarScheduleItem: { ok: true },
    },
    update(cache, _, { variables }) {
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
              (s) => s !== variables.id,
            ),
          },
        },
      });
    },
  });

  const toggleEventFavorite = (item: Item) => {
    if (!isLoggedIn) {
      router.push(`/login?next=/schedule/${day}`);
      return;
    }

    const starred = starredScheduleItems.includes(item.id);

    if (!starred) {
      starScheduleItem({
        variables: { id: item.id },
      });
    } else {
      unstarScheduleItem({
        variables: { id: item.id },
      });
    }
  };

  const [viewMode, setViewMode] = useState<ViewMode>("grid");
  const prevViewMode = useRef(null);

  const toggleScheduleView = useCallback(() => {
    setViewMode((current) => {
      const nextValue = current === "grid" ? "list" : "grid";
      prevViewMode.current = nextValue;
      va.track("schedule-view", { view: nextValue });
      return nextValue;
    });
  }, []);

  useEffect(() => {
    const listener = () => {
      const liveSlot = findLiveSlot({ currentDay, slots: day.slots });
      setLiveSlot(liveSlot);
    };

    const updateTimer = setInterval(listener, 1000 * 30);
    listener();
    const visibilityListener = () => {
      if (!document.hidden) {
        listener();
      }
    };
    document.addEventListener("visibilitychange", visibilityListener);

    return () => {
      if (updateTimer) {
        clearInterval(updateTimer);
      }

      document.removeEventListener("visibilitychange", visibilityListener);
    };
  }, []);

  if (!schedule) {
    return null;
  }

  const { days } = schedule.conference!;
  const day = days.find((d) => d.day === currentDay);
  const [currentFilters, setCurrentFilters] = useState({});
  const applyFilters = (newFilters: Record<string, string[]>) => {
    setCurrentFilters(newFilters);
  };
  const filters = [
    {
      id: "search",
      label: <FormattedMessage id="scheduleView.filter.search" />,
      search: true,
    },
    {
      id: "starred",
      label: <FormattedMessage id="scheduleView.filter.byStarred" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        {
          label: <FormattedMessage id="scheduleView.filter.starred" />,
          value: "yes",
        },
        {
          label: <FormattedMessage id="scheduleView.filter.notStarred" />,
          value: "no",
        },
      ],
    },
    {
      id: "audienceLevel",
      label: <FormattedMessage id="scheduleView.filter.byAudience" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        ...schedule.conference.audienceLevels.map((level) => ({
          label: level.name,
          value: level.id,
        })),
      ],
    },
    {
      id: "language",
      label: <FormattedMessage id="scheduleView.filter.byLanguage" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        {
          label: <FormattedMessage id="global.english" />,
          value: "en",
        },
        {
          label: <FormattedMessage id="global.italian" />,
          value: "it",
        },
      ],
    },
    {
      id: "type",
      label: <FormattedMessage id="scheduleView.filter.byType" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        {
          label: "Talk",
          value: "talk",
        },
        {
          label: "Workshop",
          value: "training",
        },
        {
          label: "Keynote",
          value: "keynote",
        },
        {
          label: "Panel",
          value: "panel",
        },
      ],
    },
  ];

  const isInMobile = useRef(null);
  useEffect(() => {
    const listener = () => {
      if (window.innerWidth < 599 && !isInMobile.current) {
        isInMobile.current = true;
        prevViewMode.current = viewMode;
        setViewMode("grid");
      } else if (window.innerWidth >= 599 && isInMobile.current) {
        isInMobile.current = false;
        setViewMode(prevViewMode.current);
      }
    };

    listener();
    window.addEventListener("resize", listener);
    return () => {
      window.removeEventListener("resize", listener);
    };
  }, [viewMode]);

  useEffect(() => {
    if (!router.isReady) {
      return;
    }

    const params = Object.entries<[string, string[]]>(currentFilters).reduce(
      (params, [key, value]) => {
        value.forEach((v: string) => params.append(key, v));
        return params;
      },
      new URLSearchParams(),
    );
    params.append("view", viewMode);

    const currentUrl = getDayUrl(currentDay, language);
    router.replace(`${currentUrl}?${params.toString()}`, undefined, {
      shallow: true,
    });
  }, [viewMode, currentFilters]);

  useEffect(() => {
    // apply filters
    if (!router.isReady) {
      return;
    }

    const params = router.query;
    console.log("params", params);

    setCurrentFilters(
      filters.reduce((acc, filter) => {
        const value = params[filter.id];
        if (!value) {
          return acc;
        }

        if (Array.isArray(value)) {
          acc[filter.id] = value;
        } else {
          acc[filter.id] = [value];
        }

        return acc;
      }, {}),
    );
    setViewMode((params.view as ViewMode) || "grid");
  }, [router.isReady]);

  const openAddToCalendarModal = () => {
    setCurrentModal("add-schedule-to-calendar");
  };

  return (
    <Fragment>
      <Section illustration="snakeHead">
        <Heading size="display1">Schedule</Heading>
        <div>
          <Spacer size="large" />
          <Text
            select="none"
            onClick={openAddToCalendarModal}
            size="label3"
            uppercase
            weight="strong"
            hoverColor="green"
          >
            <FormattedMessage id="schedule.addToCalendar" />
          </Text>
        </div>
      </Section>

      <Section noContainer>
        <DaysSelector
          days={days.map((d) => ({
            date: d.day,
            selected: d.day === currentDay,
          }))}
          onClick={changeDay}
          language={language}
        >
          <div className="shrink-0 my-3 pl-4 md:pr-4 flex md:items-center md:justify-end">
            <div className="hidden md:block">
              <Text
                select="none"
                onClick={toggleScheduleView}
                size="label3"
                uppercase
                weight="strong"
                hoverColor="green"
              >
                {viewMode === "grid" && (
                  <FormattedMessage id="schedule.listView" />
                )}
                {viewMode === "list" && (
                  <FormattedMessage id="schedule.gridView" />
                )}
              </Text>

              <Spacer size="large" orientation="horizontal" />
            </div>
            <FilterBar
              placement="left"
              onApply={applyFilters}
              appliedFilters={currentFilters}
              filters={filters}
            />
          </div>
        </DaysSelector>
        <Spacer size="large" />

        {day && (
          <div>
            {viewMode === "grid" && (
              <Schedule
                slots={day.slots}
                rooms={day.rooms}
                currentDay={currentDay}
                currentFilters={currentFilters}
                starredScheduleItems={starredScheduleItems}
                toggleEventFavorite={toggleEventFavorite}
                liveSlot={liveSlot}
              />
            )}
            {viewMode === "list" && (
              <ScheduleList
                rooms={day.rooms}
                currentDay={currentDay}
                slots={day.slots}
                currentFilters={currentFilters}
                starredScheduleItems={starredScheduleItems}
                toggleEventFavorite={toggleEventFavorite}
                liveSlot={liveSlot}
              />
            )}
          </div>
        )}
      </Section>
    </Fragment>
  );
};

export const findLiveSlot = ({
  currentDay,
  slots,
}: {
  currentDay: string;
  slots: Slot[];
}): Slot | undefined => {
  const now = new Date();
  return slots.find((slot) => {
    const startHour = fromZonedTime(
      parseISO(`${currentDay}T${slot.hour}`),
      "Europe/Rome",
    );
    const endHour = fromZonedTime(
      parseISO(`${currentDay}T${slot.endHour}`),
      "Europe/Rome",
    );

    return isAfter(now, startHour) && isBefore(now, endHour);
  });
};

export const isItemVisible = (
  item: Item,
  currentFilters: Record<string, string[]>,
  isStarred: boolean,
) => {
  if (item.type === "custom") {
    // always show custom items
    return true;
  }

  if (currentFilters.starred?.length) {
    const choice = currentFilters.starred[0];
    // if the user is filtering by starred items, we need to check if the item is starred
    if (choice === "no" && isStarred) {
      // the user wants items not starred and this is one
      return false;
    }

    if (choice === "yes" && !isStarred) {
      // the user wants starred items and this is not one
      return false;
    }
  }

  if (
    currentFilters.language?.length &&
    !currentFilters.language.includes(item.language.code)
  ) {
    return false;
  }

  if (currentFilters.type?.length && !currentFilters.type.includes(item.type)) {
    return false;
  }

  if (
    currentFilters.audienceLevel?.length &&
    !currentFilters.audienceLevel.includes(
      item.submission?.audienceLevel?.id ?? item.audienceLevel?.id,
    )
  ) {
    return false;
  }

  if (currentFilters.search?.length) {
    const query = currentFilters.search[0].toLowerCase().split(" ");
    const title = item.title.toLowerCase();
    const speakersNames = item.speakers
      .reduce((acc, speaker) => `${acc} ${speaker.fullName}`, "")
      .toLowerCase();

    if (
      !query.some(
        (word) => title.includes(word) || speakersNames.includes(word),
      ) &&
      !item.submission?.tags?.some((tag) =>
        query.some((word) => tag.name.toLowerCase().includes(word)),
      )
    ) {
      return false;
    }
  }

  return true;
};
