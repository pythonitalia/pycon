import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { InvitationLetterBuilder } from "./builder";
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
