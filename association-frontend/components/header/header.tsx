import Button from "../button/button";
import CloseIcon from "../icons/close";
import MenuIcon from "../icons/menu";
import Link from "../link/link";
import Logo from "../logo/logo";
import MenuItem from "./menu-item";
import MenuLink from "./menu-link";
import clsx from "clsx";
import React, { useState } from "react";

const MobileMenu = () => {
  const [toggleMenu, setToggleMenu] = useState(false);

  {
    /*
Mobile menu, show/hide based on mobile menu state.

Entering: "duration-200 ease-out"
From: "opacity-0 scale-95"
To: "opacity-100 scale-100"
Leaving: "duration-100 ease-in"
From: "opacity-100 scale-100"
To: "opacity-0 scale-95"
*/
  }
  if (!toggleMenu) {
    return (
      <div className="-mr-2 -my-2 md:hidden">
        <Button className={"bg-white"} onClick={() => setToggleMenu(true)}>
          <span className="sr-only">Open menu</span>
          <MenuIcon />
        </Button>
      </div>
    );
  }

  return (
    <div className="absolute z-30 top-0 inset-x-0 p-2 transition transform origin-top-right md:hidden sd:hidden">
      <div className="rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 bg-white divide-y-2 divide-gray-50">
        <div className="pt-5 pb-6 px-5">
          <div className="flex items-center justify-between">
            <div>
              <img
                className="h-8 w-auto rounded-md"
                src="/favicon.png"
                alt="home"
              />
            </div>
            <div className="-mr-2">
              <Button onClick={() => setToggleMenu(false)}>
                <span className="sr-only">Close menu</span>
                {/* Heroicon name: outline/x */}
                <CloseIcon />
              </Button>
              {/* <button
                type="button"
                className={clsx(
                  "bg-white",
                  "focus:outline-none",
                  "focus:ring-2",
                  "focus:ring-indigo-500",
                  "focus:ring-inset",
                  "hover:bg-gray-100",
                  "hover:text-gray-500",
                  "inline-flex",
                  "items-center",
                  "justify-center",
                  "p-2",
                  "rounded-md",
                  "text-gray-400",
                )}
              >
              </button> */}
            </div>
          </div>
          <div className="mt-6 sm:hidden">
            <nav className="grid grid-cols-1 gap-7 ">
              <MenuItem title={"Mail me"} description={"hello"} />
            </nav>
          </div>
        </div>
        {/* mobile! */}
        <div className="py-6 px-5">
          <div className="grid grid-cols-2 gap-4 sm:hidden">
            <MenuLink />
          </div>
          <div className="mt-6 ">
            <Button>
              <a href="/signup">Sign up</a>
            </Button>
            <p className="mt-6 text-center text-base font-medium text-gray-500">
              Already have an account?{" "}
              <a href="/login" className="text-gray-900">
                Sign in
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const Header = () => {
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
            <Button>
              <a href="/login">Sign in</a>
            </Button>

            <Button>
              <a href="/signup">Sign up</a>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
