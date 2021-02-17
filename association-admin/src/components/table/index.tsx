import classnames from "classnames";
import { Fragment, useState } from "react";
import { UrlObject } from "url";

import Link from "next/link";

import { clamp } from "~/helpers/clamp";

export type Pagination = {
  after: number;
  to: number;
  totalCount: number;
  hasMore: boolean;
  goNext: () => void;
  goBack: () => void;
};

type Props<ItemType> = {
  headers: string[];
  data: any[];
  rowGetter: (item: ItemType) => any[];
  keyGetter: (item: ItemType) => string;
  clickableItem?: (item: ItemType) => string | UrlObject;
  border?: boolean;
  pagination?: Pagination | null;
};

export const Table = <ItemType,>({
  headers,
  data,
  rowGetter,
  keyGetter,
  clickableItem,
  border = false,
  pagination = null,
}: Props<ItemType>) => {
  return (
    <div
      className={classnames({
        "rounded-lg border-gray-200 shadow": border,
      })}
    >
      <table
        className={classnames("w-full min-w-full table-fixed", {
          "overflow-hidden": border,
        })}
      >
        <thead>
          <tr
            className={classnames("border-gray-200", {
              "border-t": !border,
            })}
          >
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
                  <LinkComponent
                    key={`${keyGetter(item)}-${index}`}
                    href={hrefInfo}
                  >
                    <td
                      key={content}
                      className={classnames(
                        "px-6 py-3 max-w-0 text-sm text-gray-500 break-all",
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
      {pagination && (
        <div className="bg-gray-50 border-t py-1 flex items-center justify-between border-gray-200 px-6">
          <div className="flex-1 flex items-center justify-between">
            <p className="text-sm text-gray-700">
              Showing
              <span
                className="font-bold"
                style={{ marginLeft: "0.2rem", marginRight: "0.2rem" }}
              >
                {pagination.after + 1}
              </span>
              to
              <span
                className="font-bold"
                style={{ marginLeft: "0.2rem", marginRight: "0.2rem" }}
              >
                {clamp(pagination.to, 0, pagination.totalCount)}
              </span>
              of
              <span
                className="font-bold"
                style={{ marginLeft: "0.2rem", marginRight: "0.2rem" }}
              >
                {pagination.totalCount}
              </span>
              results
            </p>
            <nav
              className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
              aria-label="Pagination"
            >
              {pagination.after !== 0 && (
                <button
                  onClick={pagination.goBack}
                  className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                >
                  <span>Previous</span>
                </button>
              )}
              {pagination.hasMore && (
                <button
                  onClick={pagination.goNext}
                  className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                >
                  <span>Next</span>
                </button>
              )}
            </nav>
          </div>
        </div>
      )}
    </div>
  );
};
