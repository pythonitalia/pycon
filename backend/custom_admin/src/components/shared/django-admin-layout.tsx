import React, { Fragment } from "react";

type Breadcrumb = {
  label: string;
  url?: string;
};

type Props = {
  children: any;
  breadcrumbs: Breadcrumb[];
};

export const DjangoAdminLayout = ({ children, breadcrumbs }: Props) => {
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
      <h1 className="text-2xl text-[#ffc]">
        <a href="/admin">PyCon Italia</a>
      </h1>
    </div>
  );
};

const Breadcrumbs = ({ breadcrumbs }: { breadcrumbs: Breadcrumb[] }) => {
  return (
    <nav aria-label="Breadcrumbs">
      <div className="py-3 px-10 text-white bg-[#79aec8]">
        <span>
          <a href="/admin">Home</a>
        </span>
        {breadcrumbs.map((breadcrumb, index) => (
          <span key={index}>
            <a href={breadcrumb.url}>{breadcrumb.label}</a>
          </span>
        ))}
      </div>
    </nav>
  );
};
