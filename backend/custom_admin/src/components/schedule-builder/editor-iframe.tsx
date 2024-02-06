import { useIframeEditor } from "./context";

export const EditorIframe = () => {
  const { visibleScheduleItemId } = useIframeEditor();

  if (!visibleScheduleItemId) {
    return null;
  }

  const baseUrl =
    document.location.ancestorOrigins?.[0] || document.location.origin;
  const itemUrl = `${baseUrl}/admin/schedule/scheduleitem/${visibleScheduleItemId}/change/`;

  return (
    <div>
      <div className="fixed top-0 left-0 w-full h-full bg-black/50 z-[500]" />
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[1000] bg-white">
        <iframe src={itemUrl} className="w-[90vw] h-[90vh]" />
      </div>
    </div>
  );
};
