import {
  Grid,
  Text,
  GridColumn,
  Heading,
  Section,
  Spacer,
  Link,
  Button,
} from "@python-italia/pycon-styleguide";
import { SnakeWithPopcorn } from "@python-italia/pycon-styleguide/illustrations";
import { useState } from "react";
import { FormattedMessage } from "react-intl";

import {
  queryLiveStreamingSection,
  useLiveStreamingSectionQuery,
} from "~/types";

export const LiveStreamingSection = () => {
  const {
    data: {
      conference: { currentDay },
    },
  } = useLiveStreamingSectionQuery({
    returnPartialData: true,
    variables: {
      code: process.env.conferenceCode,
    },
    pollInterval: 1000 * 60 * 3,
  });
  const [currentRoom, setCurrentRoom] = useState(currentDay?.rooms?.[0]);

  const changeRoom = (newRoom) => {
    setCurrentRoom(newRoom);
  };

  const runningEvent = currentDay?.runningEvents?.filter((event) =>
    event.rooms.map((room) => room.id).includes(currentRoom.id),
  )?.[0];

  return (
    <Section>
      <Heading size="display1">Live</Heading>
      <Spacer size="2xl" />
      {!currentDay && (
        <>
          <Heading size={4}>
            <FormattedMessage id="streaming.noStreaming" />
          </Heading>
          <Spacer size="small" />
          <Link href="https://www.youtube.com/pythonitalia" target="_blank">
            <Button size="small" role="secondary">
              YouTube
            </Button>
          </Link>
        </>
      )}
      {currentDay && (
        <Grid cols={12}>
          <GridColumn colSpan={4}>
            <ul>
              {currentDay.rooms
                .filter((room) => room.streamingUrl)
                .map((room) => (
                  <li
                    className="border-b py-8 cursor-pointer"
                    onClick={(_) => changeRoom(room)}
                  >
                    <Heading
                      size={4}
                      color={room.id === currentRoom?.id ? "black" : "grey-500"}
                      className="hover:text-black transition-colors"
                    >
                      <FormattedMessage
                        id="streaming.roomName"
                        values={{
                          name: room.name,
                        }}
                      />
                    </Heading>
                  </li>
                ))}
            </ul>
          </GridColumn>
          <GridColumn colSpan={8} className="relative">
            <SnakeWithPopcorn className="absolute top-0 -translate-y-[78%] right-0 z-10" />
            <div>
              <div className="z-20 relative">
                {currentRoom && (
                  <iframe
                    height="320px"
                    src={currentRoom.streamingUrl}
                    allowFullScreen
                    scrolling="no"
                    className="aspect-video p-[3px] pt-[4px] top-0 left-0 w-full h-full bg-black"
                  />
                )}
                {runningEvent && (
                  <div>
                    <Spacer size="small" />
                    <Text as="p" size="label2">
                      <FormattedMessage
                        id="streaming.eventName"
                        values={{
                          name: (
                            <Text size="label2" weight="strong">
                              {runningEvent.title}
                            </Text>
                          ),
                        }}
                      />
                    </Text>
                    <Spacer size="xs" />
                    {runningEvent.slidoUrl && (
                      <Link href={runningEvent.slidoUrl} target="_blank">
                        <Button role="secondary" size="small">
                          <FormattedMessage id="streaming.qa" />
                        </Button>
                      </Link>
                    )}
                  </div>
                )}
              </div>
            </div>
          </GridColumn>
        </Grid>
      )}
    </Section>
  );
};

LiveStreamingSection.dataFetching = (client) => {
  return [
    queryLiveStreamingSection(client, {
      code: process.env.conferenceCode,
    }),
  ];
};
