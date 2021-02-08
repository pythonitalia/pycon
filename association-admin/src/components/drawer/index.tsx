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
                <svg
                  className="mr-3 h-4 w-4 text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                    clipRule="evenodd"
                  />
                </svg>
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
                  <svg
                    className="text-gray-500 mr-3 h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                    />
                  </svg>
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
