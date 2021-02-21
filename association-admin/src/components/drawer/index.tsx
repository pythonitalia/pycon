import classnames from "classnames";
import { LogoutOutline, UserGroupOutline } from "heroicons-react";

import Link from "next/link";
import { useRouter } from "next/router";

import { useIsOnLogin } from "~/hooks/use-is-on-login";

import { Logo } from "../logo";

const MENU_ITEMS = [
  { icon: UserGroupOutline, label: "Users", path: "/dashboard/users" },
  { icon: LogoutOutline, label: "Logout", path: "/logout" },
];

export const Drawer = () => {
  const { pathname } = useRouter();
  const isOnLogin = useIsOnLogin();

  if (isOnLogin) {
    return null;
  }

  return (
    <div className="flex-shrink-0 flex flex-col px-3 w-52 border-r border-gray-200 pt-4 pb-4 bg-gray-100">
      <div className="h-0 flex-1 flex flex-col flex-shrink-0 overflow-y-auto">
        <Logo />

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
                    {menuItem.label}
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
