import { Head } from "@inertiajs/react";

import { AppSidebar } from "@/components/app-sidebar";
import { ConferenceAnalytics } from "@/components/conference-analytics";
import { ConferenceComparisonPicker } from "@/components/conference-comparison-picker";
import type { ConferenceData } from "@/components/conference-switcher";
import type { DashboardConferenceData } from "@/components/conference-timeline";
import { ConferenceTimeline } from "@/components/conference-timeline";
import type { NavUserData } from "@/components/nav-user";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { TooltipProvider } from "@/components/ui/tooltip";
import { formatConferenceDateRange } from "@/conference-dates";

export default function Dashboard({
  comparisonConferences,
  conferences,
  maxComparisonConferences,
  selectedConference,
  user,
}: {
  comparisonConferences: DashboardConferenceData[];
  conferences: ConferenceData[];
  maxComparisonConferences: number;
  selectedConference: DashboardConferenceData | null;
  user: NavUserData;
}) {
  const pageTitle = selectedConference?.name ?? "Dashboard";

  return (
    <>
      <Head title={pageTitle} />
      <TooltipProvider>
        <SidebarProvider className="antialiased">
          <AppSidebar
            comparisonCodes={comparisonConferences.map(
              (conference) => conference.code,
            )}
            conferences={conferences}
            selectedConference={selectedConference}
            user={user}
          />
          <SidebarInset className="isolate overflow-hidden">
            <header className="flex h-14 shrink-0 items-center gap-2 border-b px-4 sm:px-6">
              <SidebarTrigger />
              <Separator
                className="data-vertical:h-4 data-vertical:self-auto"
                orientation="vertical"
              />
              <div className="flex min-w-0 flex-1 flex-col sm:flex-row sm:items-baseline sm:gap-2">
                <h1 className="truncate text-base font-medium">{pageTitle}</h1>
                {selectedConference ? (
                  <p className="truncate text-base text-muted-foreground sm:text-sm">
                    {[
                      selectedConference.location,
                      formatConferenceDateRange(
                        selectedConference.startDate,
                        selectedConference.endDate,
                      ),
                    ]
                      .filter(Boolean)
                      .join(" · ")}
                  </p>
                ) : null}
              </div>
              {selectedConference && maxComparisonConferences > 0 ? (
                <div className="flex shrink-0 items-center gap-2">
                  <ConferenceComparisonPicker
                    comparisonConferences={comparisonConferences}
                    conferences={conferences}
                    maxComparisonConferences={maxComparisonConferences}
                    selectedConference={selectedConference}
                  />
                </div>
              ) : null}
            </header>
            <main className="flex flex-1 flex-col gap-6 pt-4 sm:pt-6 lg:pt-8">
              {selectedConference ? (
                <>
                  <ConferenceTimeline conference={selectedConference} />
                  <ConferenceAnalytics
                    comparisonConferences={comparisonConferences}
                    conference={selectedConference}
                  />
                </>
              ) : (
                <section
                  aria-labelledby="empty-dashboard-title"
                  id="empty-dashboard"
                >
                  <h2
                    className="text-2xl font-semibold tracking-tight"
                    id="empty-dashboard-title"
                  >
                    No conference selected
                  </h2>
                  <p className="text-pretty text-base text-muted-foreground sm:text-sm">
                    Add a conference to see its planning timeline.
                  </p>
                </section>
              )}
            </main>
          </SidebarInset>
        </SidebarProvider>
      </TooltipProvider>
    </>
  );
}
