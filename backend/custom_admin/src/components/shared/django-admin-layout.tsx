import clsx from "clsx";
import React, { Fragment } from "react";
import { getArg } from "./get-arg";

type Breadcrumb = {
  title: string;
  url?: string;
};

type Props = {
  children: any;
};

export const DjangoAdminLayout = ({ children }: Props) => {
  const breadcrumbs: Breadcrumb[] = getArg("breadcrumbs");
  return (
    <div>
      <Header />
      <Breadcrumbs breadcrumbs={breadcrumbs} />
      <div className="py-3 px-10">{children}</div>
    </div>
  );
};

const Header = () => {
  return (
    <div className="py-3 px-10 bg-[#417690]">
      <a className="text-2xl font-light text-[#f5dd5d]" href="/admin">
        PyCon Italia
      </a>
    </div>
  );
};

const Breadcrumbs = ({ breadcrumbs }: { breadcrumbs: Breadcrumb[] }) => {
  return (
    <nav aria-label="Breadcrumbs">
      <div className="py-3 px-10 text-white bg-[#79aec8]">
        <span>
          <a
            className="hover:text-[#c4dce8] transition-colors text-sm"
            href="/admin"
          >
            Home
          </a>
        </span>
        <span>{" \u203a "}</span>
        {breadcrumbs.map((breadcrumb, index) => {
          const last = index === breadcrumbs.length - 1;
          return (
            <span key={index}>
              <a
                href={breadcrumb.url}
                className={clsx(
                  "hover:text-[#c4dce8] transition-colors text-sm",
                  {
                    "text-[#c4dce8]": last,
                  },
                )}
              >
                {breadcrumb.title}
              </a>
              {!last && <span>{" \u203a "}</span>}
            </span>
          );
        })}
      </div>
    </nav>
  );
};
