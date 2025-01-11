import { Button } from "@radix-ui/themes";
import { Box } from "@radix-ui/themes";
import { useEffect } from "react";

import { Spacer } from "../shared/spacer";
import { DocumentSettings } from "./document-settings";
import { useLocalData } from "./local-state";
import { Pages } from "./pages";

export const InvitationLetterBuilder = () => {
  const { isDirty, saveChanges, isSaving } = useLocalData();

  useEffect(() => {
    const listener = (e) => {
      if (isDirty) {
        e.preventDefault();
        e.returnValue = "";
      }

      return "";
    };

    window.addEventListener("beforeunload", listener);

    return () => {
      window.removeEventListener("beforeunload", listener);
    };
  }, [isDirty]);

  return (
    <>
      <Spacer />

      <DocumentSettings />

      <Spacer size={5} />

      <Pages />

      <Spacer />

      <Box position="sticky" bottom="0" p="3" className="bg-white">
        <Button onClick={saveChanges} loading={isSaving}>
          Save changes
        </Button>
      </Box>
    </>
  );
};
