/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Button, Flex, Heading } from "@theme-ui/components";
import React, { useLayoutEffect, useState } from "react";
import { DndProvider } from "react-dnd";
import Backend from "react-dnd-html5-backend";
import { jsx } from "theme-ui";

import { useConference } from "../../context/conference";
import {
  ScheduleQuery,
  ScheduleQueryVariables,
} from "../../generated/graphql-backend";
import { DaySelector } from "./day-selector";
import { AllTracksEvent, Talk } from "./events";
import { Schedule } from "./schedule";
import SCHEDULE_QUERY from "./schedule.graphql";
import { useSlots } from "./use-slots";

export const ScheduleScreen: React.SFC<RouteComponentProps> = () => {
  const { code } = useConference();

  const [slots, addSlot] = useSlots();
  // TODO: redirect to today or first day when we add per day routes
  const [currentDay, setCurrentDay] = useState<string | null>(null);

  const { loading, data, error } = useQuery<
    ScheduleQuery,
    ScheduleQueryVariables
  >(SCHEDULE_QUERY, {
    variables: {
      code,
    },
  });

  useLayoutEffect(() => {
    if (!currentDay && data?.conference) {
      setCurrentDay(data.conference.days[0].day);
    }
  }, [data]);

  if (loading) {
    return <Box>Loading</Box>;
  }

  if (error) {
    throw error;
  }

  const { rooms, days } = data?.conference!;

  return (
    <DndProvider backend={Backend}>
      <Box
        sx={{
          position: "fixed",
          bottom: 0,
          left: 0,
          right: 0,
          zIndex: 100,
          padding: 4,
          background: "white",
        }}
      >
        List of talks
        <Box sx={{ overflowY: "scroll", whiteSpace: "nowrap", py: 3 }}>
          {new Array(100).fill(null).map((_, index) => (
            <React.Fragment key={index}>
              <Talk duration={45} />
              <Talk duration={30} />
              <Talk duration={60} />

              <AllTracksEvent />
            </React.Fragment>
          ))}
        </Box>
      </Box>

      <Box sx={{ flex: 1 }}>
        <Box sx={{ backgroundColor: "orange", borderTop: "primary" }}>
          <Flex sx={{ py: 4, px: 3, maxWidth: "largeContainer", mx: "auto" }}>
            <Heading sx={{ fontSize: 6 }}>Schedule</Heading>

            <DaySelector
              days={days}
              currentDay={currentDay}
              setCurrentDay={setCurrentDay}
            />
          </Flex>
        </Box>

        <Schedule slots={slots} rooms={rooms} />

        <Box mt={4}>
          <Button sx={{ mr: 3 }} onClick={() => addSlot(30)}>
            Add 30 minutes slot
          </Button>
          <Button sx={{ mr: 3 }} onClick={() => addSlot(45)}>
            Add 45 minutes slot
          </Button>
          <Button sx={{ mr: 3 }} onClick={() => addSlot(60)}>
            Add 60 minutes slot
          </Button>
        </Box>
      </Box>
    </DndProvider>
  );
};
