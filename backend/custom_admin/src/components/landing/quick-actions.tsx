import type { QuickLink } from "./types";

type Props = {
  links: QuickLink[];
};

export const QuickActions = ({ links }: Props) => {
  return (
    <section>
      <h2 className="text-base font-medium text-gray-700 mb-3">
        Quick actions
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {links.map((link) => (
          <a
            key={link.title}
            href={link.url}
            className="block rounded-lg border border-gray-200 bg-white px-4 py-3 shadow-sm hover:border-[#417690] hover:shadow transition-colors"
          >
            <div className="font-medium text-[#417690]">{link.title}</div>
            <div className="text-xs text-gray-500 mt-1">{link.description}</div>
          </a>
        ))}
      </div>
    </section>
  );
};
