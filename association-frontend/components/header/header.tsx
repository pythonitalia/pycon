import { useUser } from "hooks/use-login";
import React from "react";

import Button from "../button/button";
import MenuItem from "./menu-item";
import MobileMenu from "./menu-mobile";

const Header = () => {
  const { user, logout } = useUser();
  console.log(user);
  return (
    <header>
      <div className="relative bg-white">
        <div className="flex justify-between items-center max-w-7xl mx-auto px-4 py-6 sm:px-6 md:justify-start md:space-x-10 lg:px-8">
          <div className="flex justify-start lg:w-0 lg:flex-1">
            <a href="/">
              <span className="sr-only">Home</span>

              <img
                className="h-8 w-auto sm:h-10  rounded-md"
                src="/favicon.png"
                alt=""
              />
            </a>
          </div>
          <MobileMenu />
          <nav className="hidden md:flex space-x-10">
            <div className="relative">
              {/* Item active: "text-gray-900", Item inactive: "text-gray-500" */}
              {/* <button
                type="button"
                className="group bg-white rounded-md text-gray-500 inline-flex items-center text-base font-medium hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <span>Solutions</span> */}
              {/*
    Heroicon name: solid/chevron-down

    Item active: "text-gray-600", Item inactive: "text-gray-400"
  */}
              {/* <svg
                  className="ml-2 h-5 w-5 text-gray-400 group-hover:text-gray-500"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button> */}
              {/*
  'Solutions' flyout menu, show/hide based on flyout menu state.

  Entering: "transition ease-out duration-200"
    From: "opacity-0 translate-y-1"
    To: "opacity-100 translate-y-0"
  Leaving: "transition ease-in duration-150"
    From: "opacity-100 translate-y-0"
    To: "opacity-0 translate-y-1"
*/}
              <div className="absolute z-10 -ml-4 mt-3 transform w-screen max-w-md lg:max-w-2xl lg:ml-0 lg:left-1/2 lg:-translate-x-1/2 md:hidden">
                <div className="rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 overflow-hidden">
                  <div className="relative grid gap-6 bg-white px-5 py-6 sm:gap-8 sm:p-8 lg:grid-cols-2">
                    <MenuItem
                      title={"Inbox"}
                      description={"Get a better..."}
                      //   icon={InboxIcon}
                    />
                  </div>
                </div>
              </div>
            </div>
            {/* <a
              href="#"
              className="text-base font-medium text-gray-500 hover:text-gray-900"
            >
              Pricing
            </a> */}
          </nav>
          <div className="hidden md:flex items-center justify-end md:flex-1 lg:w-0">
            {user && <Button onClick={() => logout()}>Log out</Button>}
            {!user && (
              <>
                <Button>
                  <a href="/login">Sign in</a>
                </Button>

                <Button>
                  <a href="/signup">Sign up</a>
                </Button>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
