import { Flex, Spinner } from "@radix-ui/themes";
import { Suspense } from "react";
import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { InvitationLetterBuilder } from "./builder";
import { LocalStateProvider } from "./local-state";

export const InvitationLetterDocumentBuilderRoot = ({
  documentId,
  breadcrumbs,
}) => {
  return (
    <Base
      args={{
        documentId,
        breadcrumbs,
      }}
    >
      <DjangoAdminLayout>
        <Suspense
          fallback={
            <Flex
              align="center"
              justify="center"
              width="100%"
              height="100%"
              position="absolute"
              top="0"
              left="0"
            >
              <Spinner size="3" />
            </Flex>
          }
        >
          <LocalStateProvider>
            <InvitationLetterBuilder />
          </LocalStateProvider>
        </Suspense>
      </DjangoAdminLayout>
    </Base>
  );
};
