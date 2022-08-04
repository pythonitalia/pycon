/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Text, Heading, Box, jsx } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Button } from "~/components/button/button";
import { formatDay } from "~/components/day-selector/format-day";
import { Link } from "~/components/link";
import { getItemUrl } from "~/components/schedule-view/events";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { querySchedule, useScheduleQuery } from "~/types";

const EasyViewSchedule = () => {
  const code = process.env.conferenceCode;
  const language = useCurrentLanguage();

  const {
    data: {
      conference: { days, timezone },
    },
  } = useScheduleQuery({
    variables: {
      code,
      fetchSubmissions: false,
      language,
    },
  });

  const openPrint = () => {
    window.print();
  };

  const sortedDays = [...days];
  sortedDays.sort((day1, day2) => (day1.day > day2.day ? 1 : 0));

  return (
    <Box sx={{ borderTop: "primary" }}>
      <Box sx={{ maxWidth: "largeContainer", p: 3, mx: "auto", fontSize: 2 }}>
        <Button
          onClick={openPrint}
          sx={{
            mb: 3,
            "@media print": {
              display: "none",
            },
          }}
        >
          <FormattedMessage
            defaultMessage="Save as pdf / print"
            id="scheduleEasy.saveAsPdf"
          />
        </Button>

        {sortedDays.map((day) => {
          return (
            <div
              sx={{
                mb: 3,
              }}
            >
              <Heading>
                <FormattedMessage
                  defaultMessage="Day: {day}"
                  id="scheduleEasy.day"
                  values={{
                    day: formatDay(day.day, language, timezone),
                  }}
                />
              </Heading>
              {day.slots.map((slot) => {
                return (
                  <ul
                    sx={{
                      my: 3,
                      listStyleType: "none",
                    }}
                  >
                    <li>
                      <Text sx={{ fontWeight: "bold" }}>{slot.hour}</Text>
                    </li>
                    <li>
                      <ul
                        sx={{
                          listStyleType: "none",
                        }}
                      >
                        {slot.items.map((item) => {
                          const itemUrl = getItemUrl(item);
                          return (
                            <li sx={{ mt: 3 }}>
                              <div>
                                <Text as="span" sx={{ fontWeight: "bold" }}>
                                  <FormattedMessage
                                    defaultMessage="Title"
                                    id="scheduleEasy.title"
                                  />
                                </Text>
                                : {item.title}
                              </div>
                              <div>
                                <Text as="span" sx={{ fontWeight: "bold" }}>
                                  <FormattedMessage
                                    defaultMessage="When"
                                    id="scheduleEasy.when"
                                  />
                                </Text>
                                : {day.day} {slot.hour}
                              </div>
                              <div>
                                <Text as="span" sx={{ fontWeight: "bold" }}>
                                  <FormattedMessage
                                    defaultMessage="Duration"
                                    id="scheduleEasy.duration"
                                  />
                                </Text>
                                :{" "}
                                <FormattedMessage
                                  defaultMessage="{duration} minutes"
                                  id="scheduleEasy.durationText"
                                  values={{
                                    duration: item.duration || slot.duration,
                                  }}
                                />
                              </div>
                              {item.type !== "custom" && (
                                <div>
                                  <Text as="span" sx={{ fontWeight: "bold" }}>
                                    <FormattedMessage
                                      defaultMessage="Type"
                                      id="scheduleEasy.type"
                                    />
                                  </Text>
                                  :{" "}
                                  {item.rooms[0].type === "talk" && (
                                    <FormattedMessage
                                      defaultMessage="Talk"
                                      id="scheduleEasy.type.talk"
                                    />
                                  )}
                                  {item.rooms[0].type === "training" && (
                                    <FormattedMessage
                                      defaultMessage="Workshop / Training"
                                      id="scheduleEasy.type.workshop"
                                    />
                                  )}
                                </div>
                              )}
                              {item.speakers.length > 0 && (
                                <div>
                                  <Text as="span" sx={{ fontWeight: "bold" }}>
                                    <FormattedMessage
                                      defaultMessage="Speaker(s)"
                                      id="scheduleEasy.speakers"
                                    />
                                  </Text>
                                  :{" "}
                                  {item.speakers
                                    .map((speaker) => speaker.fullName)
                                    .join(", ")}
                                </div>
                              )}
                              <div>
                                <Text as="span" sx={{ fontWeight: "bold" }}>
                                  <FormattedMessage
                                    defaultMessage="Room(s)"
                                    id="scheduleEasy.rooms"
                                  />
                                </Text>
                                :{" "}
                                {item.rooms.map((room) => room.name).join(", ")}
                              </div>
                              {item.language && (
                                <div>
                                  <Text as="span" sx={{ fontWeight: "bold" }}>
                                    <FormattedMessage
                                      defaultMessage="Language"
                                      id="scheduleEasy.language"
                                    />
                                    :{" "}
                                  </Text>
                                  <Text as="span">{item.language.name}</Text>
                                </div>
                              )}
                              {item.hasLimitedCapacity && (
                                <div>
                                  <Text as="span" sx={{ fontWeight: "bold" }}>
                                    <FormattedMessage
                                      defaultMessage="🚨 Requires booking"
                                      id="scheduleEasy.requiresBooking"
                                    />
                                    :{" "}
                                  </Text>
                                  <Text as="span">
                                    <FormattedMessage
                                      defaultMessage="This event has limited capacity. Use the link below to book a slot. (Spaces left: {spacesLeft})"
                                      id="scheduleEasy.bookingInstructions"
                                      values={{ spacesLeft: item.spacesLeft }}
                                    />
                                  </Text>
                                </div>
                              )}
                              {itemUrl && (
                                <div>
                                  <Text as="span" sx={{ fontWeight: "bold" }}>
                                    <FormattedMessage
                                      defaultMessage="Link"
                                      id="scheduleEasy.link"
                                    />
                                    :{" "}
                                  </Text>
                                  <Link
                                    path={itemUrl}
                                    params={{ slug: item.slug, day: day.day }}
                                  >
                                    https://pycon.it/talk/{item.slug}?day=
                                    {day.day}
                                  </Link>
                                </div>
                              )}
                            </li>
                          );
                        })}
                      </ul>
                    </li>
                  </ul>
                );
              })}
            </div>
          );
        })}
      </Box>
    </Box>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    querySchedule(client, {
      code: process.env.conferenceCode,
      fetchSubmissions: false,
      language: locale,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default EasyViewSchedule;
