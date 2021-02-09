import { SearchOutline, UserGroupOutline } from "heroicons-react";

import Link from "next/link";
import { useRouter } from "next/router";

import { useDrawer } from "./context";

export const Drawer = () => {
  const { pathname } = useRouter();
  const { open } = useDrawer();

  if (!open || pathname === "/login") {
    return null;
  }

  return (
    <div className="flex lg:flex-shrink-0">
      <div className="flex flex-col w-64 border-r border-gray-200 pt-5 pb-4 bg-gray-100">
        <div className="flex items-center flex-shrink-0 px-6">
          <img
            className="h-8 w-auto"
            src="https://tailwindui.com/img/logos/workflow-logo-purple-500-mark-gray-700-text.svg"
            alt="Workflow"
          />
        </div>

        <div className="h-0 flex-1 flex flex-col overflow-y-auto">
          <div className="px-3 mt-5">
            <div className="mt-1 relative rounded-md shadow-sm">
              <div
                className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                aria-hidden="true"
              >
                <SearchOutline className="mr-3 h-4 w-4 text-gray-400 stroke-current" />
              </div>
              <input
                type="text"
                name="search"
                id="search"
                className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-9 sm:text-sm border-gray-300 rounded-md"
                placeholder="Search"
              />
            </div>
          </div>

          <nav className="px-3 mt-6">
            <div className="space-y-1">
              <Link href="/dashboard/users">
                <div className="cursor-pointer bg-gray-200 text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md">
                  <UserGroupOutline
                    size={24}
                    className="mr-3 text-gray-500 stroke-current"
                  />
                  Users
                </div>
              </Link>
            </div>
          </nav>
        </div>
      </div>
    </div>
  );
};
