import { useArgs } from "../shared/args";
import { AllModels } from "./all-models";
import { GroupCard } from "./group-card";
import { QuickActions } from "./quick-actions";
import { StatCard } from "./stat-card";
import type { AdminApp, Group, QuickLink } from "./types";

// Placeholder metrics. Real values are wired in a follow-up (T5) via the
// /admin/graphql endpoint; the layout is sized for them now.
const PLACEHOLDER_STATS = [
  { label: "Submissions" },
  { label: "Grants pending" },
  { label: "Schedule items" },
  { label: "Tickets sold" },
];

export const Dashboard = () => {
  const {
    groups = [],
    quickLinks = [],
    allApps = [],
  } = useArgs() as {
    groups: Group[];
    quickLinks: QuickLink[];
    allApps: AdminApp[];
  };

  return (
    <div className="flex flex-col gap-8">
      <section>
        <h2 className="text-base font-medium text-gray-700 mb-3">Overview</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {PLACEHOLDER_STATS.map((stat) => (
            <StatCard key={stat.label} label={stat.label} />
          ))}
        </div>
      </section>

      {quickLinks.length > 0 && <QuickActions links={quickLinks} />}

      <section>
        <h2 className="text-base font-medium text-gray-700 mb-3">
          Manage by area
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {groups.map((group) => (
            <GroupCard key={group.title} group={group} />
          ))}
        </div>
      </section>

      <AllModels apps={allApps} />
    </div>
  );
};
