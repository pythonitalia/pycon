import type { AdminModel, Group } from "./types";

const ModelRow = ({ model }: { model: AdminModel }) => {
  return (
    <li className="flex items-center justify-between py-1.5 border-b border-gray-100 last:border-0">
      {model.admin_url ? (
        <a
          href={model.admin_url}
          className="text-[#417690] hover:underline truncate"
        >
          {model.name}
        </a>
      ) : (
        <span className="text-gray-700 truncate">{model.name}</span>
      )}
      {model.add_url && (
        <a
          href={model.add_url}
          className="text-xs text-gray-400 hover:text-[#417690] shrink-0 ml-2"
          aria-label={`Add ${model.name}`}
        >
          + Add
        </a>
      )}
    </li>
  );
};

export const GroupCard = ({ group }: { group: Group }) => {
  return (
    <div className="rounded-lg border border-gray-200 bg-white shadow-sm overflow-hidden">
      <div className="px-4 py-2.5 bg-[#417690] text-white font-medium">
        {group.title}
      </div>
      <ul className="px-4 py-2">
        {group.models.map((model) => (
          <ModelRow
            key={`${model.app_label}.${model.object_name}`}
            model={model}
          />
        ))}
      </ul>
    </div>
  );
};
