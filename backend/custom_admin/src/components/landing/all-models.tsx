import type { AdminApp } from "./types";

type Props = {
  apps: AdminApp[];
};

// Full stock app/model list, collapsed by default, for completeness and to keep
// rarely-used models reachable even when they aren't featured in a group.
export const AllModels = ({ apps }: Props) => {
  if (apps.length === 0) {
    return null;
  }

  return (
    <details className="rounded-lg border border-gray-200 bg-white shadow-sm">
      <summary className="cursor-pointer select-none px-4 py-3 font-medium text-gray-700">
        All models
      </summary>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-4 px-4 pb-4">
        {apps.map((app) => (
          <div key={app.app_label}>
            <div className="text-xs uppercase tracking-wide text-gray-500 mb-1">
              {app.name}
            </div>
            <ul>
              {app.models.map((model) => (
                <li key={model.object_name} className="py-0.5">
                  {model.admin_url ? (
                    <a
                      href={model.admin_url}
                      className="text-[#417690] hover:underline"
                    >
                      {model.name}
                    </a>
                  ) : (
                    <span className="text-gray-700">{model.name}</span>
                  )}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </details>
  );
};
