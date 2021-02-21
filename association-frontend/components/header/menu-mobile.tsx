import Button from "../button/button";
import CloseIcon from "../icons/close";
import MenuIcon from "../icons/menu";
import MenuItem from "./menu-item";
import MenuLink from "./menu-link";
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

export default MobileMenu;
