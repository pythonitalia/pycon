import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { Dashboard } from "./dashboard";

type Props = {
  groups: string;
  quickLinks: string;
  allApps: string;
  breadcrumbs: string;
};

export const LandingRoot = ({
  groups,
  quickLinks,
  allApps,
  breadcrumbs,
}: Props) => {
  return (
    <Base args={{ groups, quickLinks, allApps, breadcrumbs }}>
      <DjangoAdminLayout>
        <Dashboard />
      </DjangoAdminLayout>
    </Base>
  );
};
