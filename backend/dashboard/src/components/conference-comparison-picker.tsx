import { router } from "@inertiajs/react";
import { GitCompareArrowsIcon } from "lucide-react";

import type { ConferenceData } from "@/components/conference-switcher";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { dashboardUrl } from "@/dashboard-url";

export function ConferenceComparisonPicker({
  comparisonConferences,
  conferences,
  maxComparisonConferences,
  selectedConference,
}: {
  comparisonConferences: ConferenceData[];
  conferences: ConferenceData[];
  maxComparisonConferences: number;
  selectedConference: ConferenceData;
}) {
  const comparisonCodes = new Set(
    comparisonConferences.map((conference) => conference.code),
  );
  const selectedCount = comparisonConferences.length + 1;
  const comparisonLimitReached =
    comparisonConferences.length >= maxComparisonConferences;

  const updateComparison = (code: string, checked: boolean) => {
    const nextCodes = new Set(comparisonCodes);

    if (checked) {
      nextCodes.add(code);
    } else {
      nextCodes.delete(code);
    }

    const orderedCodes = conferences
      .filter((conference) => nextCodes.has(conference.code))
      .map((conference) => conference.code);

    router.visit(
      dashboardUrl(selectedConference.code, {
        comparisonCodes: orderedCodes,
      }),
      {
        preserveScroll: true,
        preserveState: true,
      },
    );
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          aria-label="Compare conferences"
          className="ml-auto"
          size="sm"
          type="button"
          variant="outline"
        >
          <GitCompareArrowsIcon aria-hidden="true" />
          <span className="hidden sm:inline">
            {comparisonConferences.length
              ? `${selectedCount} conferences`
              : "Compare"}
          </span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-72">
        <DropdownMenuLabel>
          Compare up to {maxComparisonConferences + 1} conferences
        </DropdownMenuLabel>
        {conferences.map((conference) => {
          const isPrimary = conference.code === selectedConference.code;

          return (
            <DropdownMenuCheckboxItem
              checked={isPrimary || comparisonCodes.has(conference.code)}
              disabled={
                isPrimary ||
                (!comparisonCodes.has(conference.code) &&
                  comparisonLimitReached)
              }
              key={conference.code}
              onCheckedChange={(checked) =>
                updateComparison(conference.code, checked === true)
              }
              onSelect={(event) => event.preventDefault()}
            >
              <div className="min-w-0 flex-1 py-1">
                <p className="truncate font-medium">{conference.name}</p>
                <p className="truncate text-xs text-muted-foreground">
                  {isPrimary ? "Primary conference" : conference.organizer}
                </p>
              </div>
            </DropdownMenuCheckboxItem>
          );
        })}
        {comparisonConferences.length ? (
          <>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              onSelect={() =>
                router.visit(dashboardUrl(selectedConference.code), {
                  preserveScroll: true,
                  preserveState: true,
                })
              }
            >
              Clear comparison
            </DropdownMenuItem>
          </>
        ) : null}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
