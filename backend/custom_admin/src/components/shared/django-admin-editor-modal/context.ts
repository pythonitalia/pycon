import React from "react";

type DjangoAdminEditorIframeContextProps = {
  url: string | null;
  isOpen: boolean;
  open: (url: string) => void;
  close: () => void;
};

export const DjangoAdminEditorContext =
  React.createContext<DjangoAdminEditorIframeContextProps>({
    url: null,
    isOpen: false,
    open: () => {},
    close: () => {},
  });

export const useDjangoAdminEditor = () => {
  return React.useContext(DjangoAdminEditorContext);
};
