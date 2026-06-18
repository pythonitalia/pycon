import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Text,
  Theme,
} from "@radix-ui/themes";
import { useEffect } from "react";

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
    <Theme
      accentColor="indigo"
      grayColor="slate"
      radius="large"
      panelBackground="translucent"
    >
      <Container size="3" py="6">
        <Box mb="6">
          <Heading size="7" mb="1">
            Invitation letter
          </Heading>
          <Text color="gray" size="3">
            Design the document attendees receive. Changes here apply to the
            generated PDF.
          </Text>
        </Box>

        <Flex direction="column" gap="5">
          <DocumentSettings />
          <Pages />
        </Flex>

        {/* Breathing room so content clears the sticky save bar */}
        <Box height="var(--space-9)" />
      </Container>

      <Box
        position="sticky"
        bottom="0"
        style={{
          borderTop: "1px solid var(--gray-a5)",
          backgroundColor: "var(--color-panel-translucent)",
          backdropFilter: "blur(8px)",
          WebkitBackdropFilter: "blur(8px)",
        }}
      >
        <Container size="3" px="5">
          <Flex align="center" justify="between" gap="3" py="3">
            <Text size="2" color={isDirty ? "amber" : "gray"}>
              {isDirty ? "You have unsaved changes" : "All changes saved"}
            </Text>
            <Button
              onClick={saveChanges}
              loading={isSaving}
              disabled={!isDirty}
              size="3"
            >
              Save changes
            </Button>
          </Flex>
        </Container>
      </Box>
    </Theme>
  );
};
