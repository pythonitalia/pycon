import type { AnalyticsChartData } from "@/components/conference-analytics";
import type { ConferenceData } from "@/components/conference-switcher";
import { formatConferenceDate } from "@/conference-dates";
import { cn } from "@/lib/utils";

type MilestoneStatus = "complete" | "current" | "upcoming";

export type ConferenceMilestoneData = {
  date: string;
  id: string;
  label: string;
  metric: string | null;
  relative: string | null;
  status: MilestoneStatus;
};

export type DashboardConferenceData = ConferenceData & {
  analytics: AnalyticsChartData[];
  countdown: {
    label: string;
    value: string;
  };
  endDate: string | null;
  location: string;
  milestones: ConferenceMilestoneData[];
  startDate: string | null;
};

export function ConferenceTimeline({
  conference,
}: {
  conference: DashboardConferenceData;
}) {
  return (
    <section
      aria-labelledby="conference-timeline-title"
      id="conference-timeline"
    >
      <h2 className="sr-only" id="conference-timeline-title">
        Conference timeline
      </h2>
      <div className="@container overflow-x-auto px-4 py-2 sm:px-6 lg:px-8">
        <ol
          aria-label="Conference milestones"
          className="flex min-w-3xl list-none"
        >
          {conference.milestones.map((milestone, index) => {
            const isFirst = index === 0;
            const isLast = index === conference.milestones.length - 1;

            return (
              <li
                aria-current={
                  milestone.status === "current" ? "step" : undefined
                }
                className={cn(
                  "min-w-0",
                  isFirst || isLast ? "flex-[1_1_0%]" : "flex-[2_1_0%]",
                )}
                key={milestone.id}
              >
                <div
                  className={cn(
                    "flex min-w-0 items-baseline gap-2 pb-4",
                    isFirst && "w-[200%] justify-start",
                    isLast &&
                      "w-[200%] -translate-x-1/2 justify-end text-right",
                    !isFirst && !isLast && "justify-center px-3 text-center",
                  )}
                >
                  <p className="shrink-0 text-base font-semibold tabular-nums sm:text-sm">
                    {formatConferenceDate(milestone.date)}
                  </p>
                  {milestone.metric ? (
                    <p className="truncate text-base text-muted-foreground tabular-nums sm:text-sm">
                      {milestone.metric}
                    </p>
                  ) : null}
                </div>
                <div className="flex items-center">
                  {isFirst ? null : (
                    <div
                      aria-hidden="true"
                      className="h-px min-w-0 flex-1 border-t border-dashed border-foreground/20"
                    />
                  )}
                  <div
                    aria-hidden="true"
                    className={cn(
                      "size-3 shrink-0 border-2 bg-background",
                      milestone.status === "complete" &&
                        "border-primary bg-primary",
                      milestone.status === "current" && "border-primary",
                      milestone.status === "upcoming" &&
                        "border-muted-foreground/30",
                    )}
                  />
                  {isLast ? null : (
                    <div
                      aria-hidden="true"
                      className="h-px flex-1 border-t border-dashed border-foreground/20"
                    />
                  )}
                </div>
                <p
                  className={cn(
                    "truncate pt-4 text-base font-medium sm:text-sm",
                    isFirst && "w-[200%] text-left",
                    isLast && "w-[200%] -translate-x-1/2 text-right",
                    !isFirst && !isLast && "px-3 text-center",
                  )}
                >
                  {milestone.label}
                </p>
              </li>
            );
          })}
        </ol>
      </div>
    </section>
  );
}
