import { useMemo, useState } from "react";

import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { Calendar } from "./calendar";
import { IframeEditorContext } from "./context";
import { EditorIframe } from "./editor-iframe";
import { useConferenceScheduleQuery } from "./schedule.generated";

export const ScheduleBuilderRoot = () => {
  const [iframeEditorVisibleScheduleItem, setVisibleScheduleItemIframeEditor] =
    useState(null);
  const iframeEditorContextValue = useMemo(
    () => ({
      visibleScheduleItemId: iframeEditorVisibleScheduleItem,
      open: (scheduleItemId) => {
        setVisibleScheduleItemIframeEditor(scheduleItemId);
      },
      close: () => {
        setVisibleScheduleItemIframeEditor(null);
      },
    }),
    [iframeEditorVisibleScheduleItem],
  );

  return (
    <Base>
      <IframeEditorContext.Provider value={iframeEditorContextValue}>
        <ScheduleBuilder />
      </IframeEditorContext.Provider>
    </Base>
  );
};

const ScheduleBuilder = () => {
  const conferenceId = (window as any).conferenceId;
  const { error, loading, data } = useConferenceScheduleQuery({
    variables: {
      conferenceId,
    },
  });

  if (loading) {
    return "wait";
  }

  console.log("error", error);

  const {
    conferenceSchedule: { days },
  } = data;
  console.log("conferenceId", days);

  return (
    <DjangoAdminLayout
      breadcrumbs={[
        { label: "Conference", url: "/admin/conferences/conference" },
        { label: "Schedule Builder" },
      ]}
    >
      <EditorIframe />

      {days.map((day) => (
        <Calendar key={day.id} day={day} />
      ))}
    </DjangoAdminLayout>
  );
};
