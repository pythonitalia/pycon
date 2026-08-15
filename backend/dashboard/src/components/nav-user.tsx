import { BadgeCheckIcon, ChevronsUpDownIcon, LogOutIcon } from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";

export type NavUserData = {
  name: string;
  email: string;
  avatar: string | null;
  profileUrl: string;
};

function getInitials(name: string) {
  return (
    name
      .split(/\s+/)
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join("") || "?"
  );
}

export function NavUser({ user }: { user: NavUserData }) {
  const { isMobile } = useSidebar();
  const initials = getInitials(user.name);

  async function logOut() {
    const response = await fetch("/graphql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: "mutation DashboardLogout { logout { ok } }",
      }),
    });

    if (response.ok) {
      window.location.assign("/dashboard/login");
    }
  }

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              className="data-open:bg-sidebar-accent data-open:text-sidebar-accent-foreground"
              size="lg"
            >
              <Avatar className="rounded-lg">
                {user.avatar ? (
                  <AvatarImage alt={user.name} src={user.avatar} />
                ) : null}
                <AvatarFallback className="rounded-lg">
                  {initials}
                </AvatarFallback>
              </Avatar>
              <div className="grid flex-1 text-left text-sm/4">
                <div className="truncate font-medium">{user.name}</div>
                <div className="truncate text-xs">{user.email}</div>
              </div>
              <ChevronsUpDownIcon className="ml-auto" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            align="end"
            className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
            side={isMobile ? "bottom" : "right"}
            sideOffset={4}
          >
            <DropdownMenuLabel className="p-0 font-normal">
              <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                <Avatar className="rounded-lg">
                  {user.avatar ? (
                    <AvatarImage alt={user.name} src={user.avatar} />
                  ) : null}
                  <AvatarFallback className="rounded-lg">
                    {initials}
                  </AvatarFallback>
                </Avatar>
                <div className="grid flex-1 text-left text-sm/4">
                  <div className="truncate font-medium">{user.name}</div>
                  <div className="truncate text-xs">{user.email}</div>
                </div>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              <a href={user.profileUrl}>
                <BadgeCheckIcon />
                Account
              </a>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onSelect={() => void logOut()}>
              <LogOutIcon />
              Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
