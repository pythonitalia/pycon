import React from "react";

type IframeEditorContextProps = {
  visibleScheduleItemId: number | null;
  open: (scheduleItemId: number) => void;
  close: () => void;
};

export const IframeEditorContext =
  React.createContext<IframeEditorContextProps>({
    visibleScheduleItemId: null,
    open: () => {},
    close: () => {},
  });

export const useIframeEditor = () => {
  return React.useContext(IframeEditorContext);
};
