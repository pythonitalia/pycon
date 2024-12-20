import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { InvitationLetterBuilder } from "./builder";
import { LocalStateProvider } from "./local-state";

export const InvitationLetterDocumentBuilderRoot = () => {
  return (
    <Base>
      <DjangoAdminLayout>
        <LocalStateProvider>
          <InvitationLetterBuilder />
        </LocalStateProvider>
      </DjangoAdminLayout>
    </Base>
  );
};
