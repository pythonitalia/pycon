import { clamp } from "~/helpers/clamp";

import { Button, ButtonVariant } from "../button";

export type Pagination = {
  after: number;
  to: number;
  totalCount: number;
  hasMore: boolean;
  goNext: () => void;
  goBack: () => void;
};

type Props = {
  pagination?: Pagination | null;
};

export const PaginationBar: React.FC<Props> = ({ pagination }) => (
  <div className="bg-gray-50 border-t py-1 flex items-center justify-between border-gray-200 px-6">
    <div className="flex-1 flex items-center justify-between">
      <p className="text-sm text-gray-700 space-x-1">
        <span>Showing</span>
        <span className="font-bold">{pagination.after + 1}</span>
        <span>to</span>
        <span className="font-bold">
          {clamp(pagination.to, 0, pagination.totalCount)}
        </span>
        <span>of</span>
        <span className="font-bold">{pagination.totalCount}</span>
        <span>results</span>
      </p>
      <nav
        className="relative z-0 inline-flex rounded-md shadow-sm space-x-2"
        aria-label="Pagination"
      >
        {pagination.after !== 0 && (
          <Button
            variant={ButtonVariant.PAGINATION}
            type="button"
            onClick={pagination.goBack}
          >
            Previous
          </Button>
        )}
        {pagination.hasMore && (
          <Button
            variant={ButtonVariant.PAGINATION}
            type="button"
            onClick={pagination.goNext}
          >
            Next
          </Button>
        )}
      </nav>
    </div>
  </div>
);
