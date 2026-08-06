import { Link } from "@inertiajs/react";
import { CheckIcon, ChevronsUpDownIcon } from "lucide-react";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";

export type ConferenceData = {
  code: string;
  name: string;
  organizer: string;
  year: number | null;
};

function getConferenceMark(conference: ConferenceData) {
  if (conference.year) {
    return String(conference.year).slice(-2);
  }

  return conference.name.slice(0, 2).toUpperCase();
}

export function ConferenceSwitcher({
  conferences,
  selectedConference,
}: {
  conferences: ConferenceData[];
  selectedConference: ConferenceData | null;
}) {
  const { isMobile } = useSidebar();

  if (!selectedConference) {
    return (
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton disabled size="lg" tooltip="No conferences">
            <div
              aria-hidden="true"
              className="flex aspect-square size-8 shrink-0 items-center justify-center rounded-lg bg-sidebar-primary text-sm font-semibold text-sidebar-primary-foreground"
            >
              --
            </div>
            <div className="grid flex-1 text-left text-sm/4">
              <div className="truncate font-semibold">No conferences</div>
              <div className="truncate text-xs text-muted-foreground">
                Python Italia
              </div>
            </div>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    );
  }

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              className="data-open:bg-sidebar-accent data-open:text-sidebar-accent-foreground"
              size="lg"
              tooltip={selectedConference.name}
            >
              <div
                aria-hidden="true"
                className="flex aspect-square size-8 shrink-0 items-center justify-center rounded-lg bg-sidebar-primary text-sm font-semibold text-sidebar-primary-foreground tabular-nums"
              >
                {getConferenceMark(selectedConference)}
              </div>
              <div className="grid flex-1 text-left text-sm/4">
                <div className="truncate font-semibold">
                  {selectedConference.name}
                </div>
                <div className="truncate text-xs text-muted-foreground">
                  {selectedConference.organizer}
                </div>
              </div>
              <ChevronsUpDownIcon className="ml-auto" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            align="start"
            className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
            side={isMobile ? "bottom" : "right"}
            sideOffset={4}
          >
            <DropdownMenuLabel>Conferences</DropdownMenuLabel>
            {conferences.map((conference) => (
              <DropdownMenuItem
                asChild
                className="gap-2 p-2"
                key={conference.code}
              >
                <Link
                  href={`/dashboard/${encodeURIComponent(conference.code)}`}
                >
                  <div
                    aria-hidden="true"
                    className="flex size-6 shrink-0 items-center justify-center rounded-md border text-xs font-medium tabular-nums"
                  >
                    {getConferenceMark(conference)}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="truncate font-medium">
                      {conference.name}
                    </div>
                    <div className="truncate text-xs text-muted-foreground">
                      {conference.organizer}
                    </div>
                  </div>
                  {conference.code === selectedConference.code ? (
                    <CheckIcon aria-label="Selected" className="ml-auto" />
                  ) : null}
                </Link>
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
