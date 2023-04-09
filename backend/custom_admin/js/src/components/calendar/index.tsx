import React, { useState } from "react";

import { DayScheduleView } from "./day-schedule-view";
import { useScheduleQuery } from "./schedule.generated";
import { SidePanel } from "./side-panel";
import { getVars } from "./vars";

export const Calendar = () => {
  const conferenceCode = getVars().conferenceCode;
  const { loading, data: scheduleData } = useScheduleQuery({
    variables: {
      code: conferenceCode,
    },
  });
  console.log("[scheduleData]", scheduleData, loading);

  if (!scheduleData) {
    return null;
  }

  return (
    <div className="mr-[200px]">
      {scheduleData.conference.days.map((day) => (
        <>
          <h2 className="font-bold bg-white p-3 border-b-4 sticky top-0 z-[100]">
            {day.day}
          </h2>
          <DayScheduleView day={day} />
          <div className="h-10" />
        </>
      ))}
      <SidePanel />
    </div>
  );
};
