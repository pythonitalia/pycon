import { useApolloClient } from "@apollo/client";
import { useEffect } from "react";

import { useIframeEditor } from "./context";

export const EditorIframe = () => {
  const { visibleScheduleItemId, close } = useIframeEditor();
  const apolloClient = useApolloClient();

  const onClose = () => {
    close();
    apolloClient.refetchQueries({
      include: ["ConferenceSchedule"],
    });
  };

  useEffect(() => {
    if (visibleScheduleItemId) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    return () => {
      document.body.style.overflow = "auto";
    };
  }, [visibleScheduleItemId]);

  if (!visibleScheduleItemId) {
    return null;
  }

  const baseUrl =
    document.location.ancestorOrigins?.[0] || document.location.origin;
  const itemUrl = `${baseUrl}/admin/schedule/scheduleitem/${visibleScheduleItemId}/change/`;

  return (
    <div>
      <div
        className="fixed top-0 left-0 w-full h-full bg-black/50 z-[500]"
        onClick={onClose}
      />
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[1000] bg-white">
        <iframe src={itemUrl} className="w-[90vw] h-[90vh] z-[100]" />
      </div>
    </div>
  );
};
