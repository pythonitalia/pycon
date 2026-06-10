import { useApolloClient } from "@apollo/client";
import { Dialog, VisuallyHidden } from "@radix-ui/themes";
import { useMemo, useState } from "react";

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
    <Dialog.Root open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <Dialog.Content maxWidth="90vw" width="90vw">
        <VisuallyHidden>
          <Dialog.Title>Admin view</Dialog.Title>
        </VisuallyHidden>
        <iframe title="Admin view" src={itemUrl} className="w-full h-[85vh]" />
      </Dialog.Content>
    </Dialog.Root>
  );
};
