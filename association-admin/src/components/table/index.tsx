import classnames from "classnames";
import { Fragment } from "react";
import { UrlObject } from "url";

import Link from "next/link";

type Props<ItemType> = {
  headers: string[];
  data: any[];
  rowGetter: (item: ItemType) => any[];
  keyGetter: (item: ItemType) => string;
  clickableItem?: (item: ItemType) => string | UrlObject;
};

// const getBgColor = (value: string) =>
//   value === "true" ? "bg-green-600" : "bg-red-600";

export const Table = <ItemType,>({
  headers,
  data,
  rowGetter,
  keyGetter,
  clickableItem,
}: Props<ItemType>) => (
  <table className="w-full min-w-full table-fixed">
    <thead>
      <tr className="border-t border-gray-200">
        {headers.map((header) => (
          <th
            key={header}
            className="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
          >
            {header}
          </th>
        ))}
      </tr>
    </thead>
    <tbody className="bg-white divide-y divide-gray-100">
      {data.map((item) => {
        // @ts-ignore
        const row = rowGetter(item);
        const hrefInfo = clickableItem?.(item);
        const LinkComponent = hrefInfo ? Link : Fragment;

        return (
          <tr
            key={keyGetter(item)}
            className={classnames("hover:bg-gray-50", {
              "cursor-pointer": hrefInfo,
            })}
          >
            {row.map((content, index) => (
              <LinkComponent href={hrefInfo}>
                <td
                  key={content}
                  className={classnames(
                    "px-6 py-3 max-w-0 text-sm select-none text-gray-500 break-all",
                    {
                      "font-medium": index === 0,
                    },
                  )}
                >
                  {content}
                </td>
              </LinkComponent>
            ))}
          </tr>
        );
      })}
    </tbody>
  </table>
);
