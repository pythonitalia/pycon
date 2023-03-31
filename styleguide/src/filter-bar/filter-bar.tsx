import clsx from "clsx";
import React, { useEffect, useState } from "react";
import { Heading } from "../heading/index";
import { BasicButton, Button } from "../button/index";
import { Text } from "../text/index";
import { Input } from "../index";
import { FormattedMessage } from "react-intl";
import { createPortal } from "react-dom";

type FilterOption = {
  label: string | React.ReactNode;
  value: string;
};

type Filter = {
  id: string;
  label: string | React.ReactNode;
  options?: FilterOption[];
  search?: boolean;
};

type Props = {
  filters: Filter[];
  appliedFilters: Record<string, string[]>;
  onApply: (changedFilters: Record<string, string[]>) => void;
  placement?: "right" | "left";
};

export const FilterBar = ({
  filters,
  appliedFilters = {},
  onApply,
  placement = "right",
}: Props) => {
  // using the state here so we can render the overlay once the dom is ready
  const [overlayElement, setOverlayElement] = useState<HTMLDivElement | null>(
    null
  );
  const [isOpen, setIsOpen] = useState(false);
  const [changedFilters, setChangedFilters] = useState(appliedFilters);
  const [isDirty, setIsDirty] = useState(false);

  useEffect(() => {
    const classes = ["overflow-hidden", "md:overflow-scroll"];

    if (isOpen) {
      document.body.classList.add(...classes);
    }

    return () => {
      document.body.classList.remove(...classes);
    };
  }, [isOpen]);

  useEffect(() => {
    const element = document.createElement("div");
    element.id = "filter-bar-overlay";
    document.body.appendChild(element);
    setOverlayElement(element);
    return () => {
      document.body.removeChild(element);
      setOverlayElement(null);
    };
  }, []);

  const changeFilter = (filterId: string, value: string) => {
    setIsDirty(true);
    const isSearchFilter = filters.find((f) => f.id === filterId)?.search;

    if (isSearchFilter) {
      setChangedFilters({
        ...changedFilters,
        [filterId]: [value],
      });
      return;
    }

    if (changedFilters[filterId]?.includes(value)) {
      setChangedFilters({
        ...changedFilters,
        [filterId]: changedFilters[filterId].filter((v) => v !== value),
      });
    } else {
      if (value === "") {
        setChangedFilters({
          ...changedFilters,
          [filterId]: [],
        });
        return;
      }

      setChangedFilters({
        ...changedFilters,
        [filterId]: [...(changedFilters[filterId] || []), value],
      });
    }
  };

  const onReset = () => {
    if (isDirty) {
      setChangedFilters(appliedFilters);
      setIsDirty(false);
    } else {
      setIsDirty(false);
      setChangedFilters({});
      onApply({});
    }
  };

  const applyChanges = () => {
    onApply(changedFilters);
    setIsOpen(false);
    setIsDirty(false);
  };

  const countFilters = Object.keys(
    Object.values(appliedFilters).filter((v) => v.length)
  ).length;

  const toggleFilterBar = () => {
    setIsOpen((value) => !value);
  };

  return (
    <>
      {overlayElement &&
        createPortal(
          <div
            onClick={toggleFilterBar}
            className={clsx(
              "fixed md:hidden inset-0 z-[1001] bg-[#1E1E1E] transition-opacity",
              {
                "opacity-0 pointer-events-none": !isOpen,
              }
            )}
          />,
          overlayElement
        )}

      <div className="md:relative inline-block select-none">
        <div
          className={
            "fixed md:relative bottom-0 left-0 w-full md:w-fit z-[300] inline-block"
          }
        >
          <div
            className="bg-milk md:bg-transparent py-8 md:py-0 flex items-center justify-center border-t md:border-t-0 cursor-pointer"
            onClick={toggleFilterBar}
          >
            <Text size="label3" uppercase weight="strong">
              <FormattedMessage id="filter.filter" defaultMessage="Filter" />
            </Text>
            {countFilters > 0 && (
              <span className="bg-[#0E1116] ml-2 rounded-full text-sm text-center inline-block text-milk w-[20px] h-[20px]">
                {countFilters}
              </span>
            )}
          </div>
        </div>
        <div
          className={clsx(
            "fixed bottom-0 left-0 md:absolute md:top-8 w-full z-[1002] md:z-[900] transition-all ease-in-out duration-300",
            {
              "translate-y-0 md:translate-y-full md:scale-100 opacity-100":
                isOpen,
              "translate-y-full opacity-0 md:scale-0": !isOpen,
              "md:origin-top-left": placement === "right",
              "md:origin-top-right": placement === "left",
            }
          )}
        >
          <div
            className={clsx(
              "md:w-[330px] w-full bg-milk border-b md:border-l md:border-r",
              {
                "md:translate-x-[calc(-100%_+_40px)]": placement === "left",
              }
            )}
          >
            <div className="max-h-[310px] overflow-scroll">
              {filters.map((filter) => (
                <>
                  <div className="bg-cream p-4 border-t border-b sticky top-0">
                    <Heading size={6}>{filter.label}</Heading>
                  </div>

                  {filter.search && (
                    <FormattedMessage
                      id="filter.searchPlaceholder"
                      defaultMessage="speaker, titles, tags"
                    >
                      {(message) => (
                        <Input
                          className="!p-4 !border-b-0"
                          showErrorBar={false}
                          placeholder={String(message)}
                          value={changedFilters[filter.id]?.[0] || ""}
                          onChange={(e) =>
                            changeFilter(filter.id, e.target.value)
                          }
                        />
                      )}
                    </FormattedMessage>
                  )}

                  {filter.options?.map((option, index) => (
                    <div
                      className={clsx(
                        "bg-milk p-4 hover:bg-neutral/20 transition-colors cursor-pointer flex items-center justify-between",
                        {
                          "border-b-1": index !== filter.options!.length - 1,
                        }
                      )}
                      onClick={() => changeFilter(filter.id, option.value)}
                    >
                      <Text size={3}>{option.label}</Text>
                      {changedFilters[filter.id]?.includes(option.value) && (
                        <Tick />
                      )}
                    </div>
                  ))}
                </>
              ))}
            </div>
            <div className="border-t px-5 py-3 flex justify-between">
              <BasicButton onClick={onReset}>
                <FormattedMessage id="filters.reset" defaultMessage="Reset" />
              </BasicButton>
              <Button size="small" role="secondary" onClick={applyChanges}>
                <FormattedMessage id="filters.apply" defaultMessage="Apply" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

const Tick = () => (
  <svg width="23" height="16" viewBox="0 0 23 16" fill="none">
    <path
      d="M1.39844 6.45555L8.99993 14.0573L21.9205 1.13672"
      stroke="#0E1116"
      strokeWidth="2"
    />
  </svg>
);
