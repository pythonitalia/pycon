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

  const baseUrl =
    document.location.ancestorOrigins?.[0] || document.location.origin;

  return (
    <Dialog.Root open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <Dialog.Content maxWidth="90vw" width="90vw">
        <VisuallyHidden>
          <Dialog.Title>Admin view</Dialog.Title>
        </VisuallyHidden>
        {/* url is null while the dialog animates closed; keep Dialog.Root
            mounted so Radix can finish closing and restore body pointer
            events — unmounting it while open leaves the page unclickable. */}
        {url && (
          <iframe
            title="Admin view"
            src={`${baseUrl}/admin${url}`}
            className="w-full h-[85vh]"
          />
        )}
      </Dialog.Content>
    </Dialog.Root>
  );
};
