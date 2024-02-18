import { useApolloClient } from "@apollo/client";
import { useEffect, useMemo, useState } from "react";

import { Modal } from "../modal";
import { DjangoAdminEditorContext, useDjangoAdminEditor } from "./context";

export const DjangoAdminEditorProvider = ({ children }) => {
  const [url, setUrl] = useState(null);

  const djangoAdminEditorState = useMemo(
    () => ({
      url,
      isOpen: !!url,
      open: (scheduleItemId) => {
        setUrl(scheduleItemId);
      },
      close: () => {
        setUrl(null);
      },
    }),
    [url],
  );

  return (
    <DjangoAdminEditorContext.Provider value={djangoAdminEditorState}>
      <DjangoAdminEditorModal />
      {children}
    </DjangoAdminEditorContext.Provider>
  );
};

export const DjangoAdminEditorModal = () => {
  const { url, close, isOpen } = useDjangoAdminEditor();
  const apolloClient = useApolloClient();

  const onClose = () => {
    close();
    apolloClient.refetchQueries({
      include: ["ConferenceSchedule"],
    });
  };

  if (!url) {
    return null;
  }

  const baseUrl =
    document.location.ancestorOrigins?.[0] || document.location.origin;
  const itemUrl = `${baseUrl}/admin${url}`;

  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <iframe
        title="Admin view"
        src={itemUrl}
        className="w-[90vw] h-[90vh] z-[100]"
      />
    </Modal>
  );
};
