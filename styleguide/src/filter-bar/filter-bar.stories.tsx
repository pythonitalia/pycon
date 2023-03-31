import React, { useState } from "react";

import { FilterBar } from "./filter-bar";

export default {
  title: "Filter Bar",
};

export const Primary = () => {
  const [appliedFilters, setAppliedFilters] = useState({});
  return (
    <div className="flex items-end justify-end">
      <FilterBar
        onApply={(newFilters) => setAppliedFilters(newFilters)}
        placement="left"
        appliedFilters={appliedFilters}
        filters={[
          {
            id: "search",
            label: "Search",
            search: true,
          },
          {
            id: "audience-level",
            label: "By Audience Level",
            options: [
              {
                label: "All",
                value: "",
              },
              {
                label: "Beginner",
                value: "beginner",
              },
              {
                label: "Intermediate",
                value: "intermediate",
              },
              {
                label: "Advanced",
                value: "advanced",
              },
            ],
          },
          {
            id: "language",
            label: "By Language",
            options: [
              {
                label: "All",
                value: "",
              },
              {
                label: "English",
                value: "english",
              },
              {
                label: "Italian",
                value: "italian",
              },
            ],
          },
          {
            id: "type",
            label: "By Type",
            options: [
              {
                label: "All",
                value: "",
              },
              {
                label: "Talk",
                value: "talk",
              },
              {
                label: "Workshop",
                value: "workshop",
              },
              {
                label: "Panel",
                value: "panel",
              },
              {
                label: "Q&A",
                value: "qa",
              },
            ],
          },
        ]}
      />
    </div>
  );
};
