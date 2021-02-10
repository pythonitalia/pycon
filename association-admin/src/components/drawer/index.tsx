import classnames from "classnames";
import { SearchOutline, UserGroupOutline } from "heroicons-react";

import Link from "next/link";
import { useRouter } from "next/router";

import { Input } from "../input";
import { Logo } from "../logo";
import { useDrawer } from "./context";

const MENU_ITEMS = [
  { icon: UserGroupOutline, label: "Users", path: "/dashboard/users" },
];

export const Drawer = () => {
  const { pathname } = useRouter();
  const { open } = useDrawer();

  if (!open || pathname === "/login") {
    return null;
  }

  return (
    <div className="lg:flex-shrink-0 flex flex-col px-3 w-50 border-r border-gray-200 pt-4 pb-4 bg-gray-100">
      <div className="h-0 flex-1 flex flex-col overflow-y-auto">
        <Logo />

        <Input
          icon={SearchOutline}
          type="text"
          name="search"
          id="search"
          placeholder="Search"
        />

        <nav className="mt-6">
          <div className="space-y-2">
            {MENU_ITEMS.map((menuItem) => {
              const Icon = menuItem.icon;
              const path = menuItem.path;
              const activePath = pathname.startsWith(menuItem.path);

              return (
                <Link href={path} key={path}>
                  <div
                    className={classnames(
                      "cursor-pointer text-sm group flex items-center px-2 rounded-md",
                      {
                        "text-gray-900": !activePath,
                        "font-bold text-blue-900": activePath,
                      },
                    )}
                  >
                    <Icon size={16} className="mr-3 stroke-current" />
                    Users
                  </div>
                </Link>
              );
            })}
          </div>
        </nav>
      </div>
    </div>
  );
};
