import { Link } from "@inertiajs/react";
import { LayoutDashboard } from "lucide-react";

import {
  type ConferenceData,
  ConferenceSwitcher,
} from "@/components/conference-switcher";
import { NavUser, type NavUserData } from "@/components/nav-user";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar";

export function AppSidebar({
  conferences,
  selectedConference,
  user,
}: {
  conferences: ConferenceData[];
  selectedConference: ConferenceData | null;
  user: NavUserData;
}) {
  const dashboardUrl = selectedConference
    ? `/dashboard/${encodeURIComponent(selectedConference.code)}`
    : "/dashboard";

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader>
        <ConferenceSwitcher
          conferences={conferences}
          selectedConference={selectedConference}
        />
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild isActive tooltip="Dashboard">
                  <Link href={dashboardUrl}>
                    <LayoutDashboard aria-hidden="true" />
                    <span>Dashboard</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <NavUser user={user} />
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  );
}
