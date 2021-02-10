import { SearchOutline, UserGroupOutline } from "heroicons-react";

import Link from "next/link";
import { useRouter } from "next/router";

import { Input } from "../input";
import { useDrawer } from "./context";

export const Drawer = () => {
  const { pathname } = useRouter();
  const { open } = useDrawer();

  if (!open || pathname === "/login") {
    return null;
  }

  return (
    <div className="lg:flex-shrink-0 flex flex-col px-3 w-64 border-r border-gray-200 pt-4 pb-4 bg-gray-100">
      <div className="h-0 flex-1 flex flex-col overflow-y-auto">
        <Input
          icon={SearchOutline}
          type="text"
          name="search"
          id="search"
          placeholder="Search"
        />

        <nav className="mt-6">
          <div className="space-y-2">
            <Link href="/dashboard/users">
              <div className="cursor-pointer bg-gray-200 text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md">
                <UserGroupOutline
                  size={24}
                  className="mr-3 text-gray-400 stroke-current"
                />
                Users
              </div>
            </Link>
          </div>
        </nav>
      </div>
    </div>
  );
};
