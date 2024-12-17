import { Heading, Text } from "@radix-ui/themes";
import { Box } from "@radix-ui/themes";
import { Fragment, useEffect, useState } from "react";
import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { InvitationLetterBuilder } from "./builder";
import { Editor } from "./editor";
import { useInvitationLetterDocumentQuery } from "./invitation-letter-document.generated";
import { LocalStateProvider } from "./local-state";

export const InvitationLetterDocumentBuilderRoot = () => {
  return (
    <Base>
      <DjangoAdminLayout
        breadcrumbs={[{ id: 0, label: "Invitation Letter Document Builder" }]}
      >
        <LocalStateProvider>
          <InvitationLetterBuilder />
        </LocalStateProvider>
      </DjangoAdminLayout>
    </Base>
  );
};
