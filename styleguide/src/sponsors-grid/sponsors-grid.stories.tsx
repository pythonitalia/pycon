import React from "react";
import { Grid, GridColumn } from "../grid";
import { SponsorsGrid } from "./sponsors-grid";

export default {
  title: "Sponsors Grid",
};

export const Default = () => (
  <SponsorsGrid
    tiers={[
      {
        name: "Keystone",
        cols: 1,
        sponsors: [
          {
            name: "Example",
            logo: "https://cdn.pycon.it/sponsors/cloudamqp-by-84codes-original.png",
            url: "https://example.org",
          },
        ],
      },
      {
        name: "Gold",
        sponsors: [
          {
            name: "Example",
            logo: "https://cdn.pycon.it/sponsors/cloudamqp-by-84codes-original.png",
            url: "https://example.org",
          },
          {
            name: "Example",
            logo: "https://cdn.pycon.it/sponsors/Manninglogo_outline.png",
            url: "https://example.org",
          },
        ],
      },
      {
        name: "Silver",
        sponsors: [
          {
            name: "Example",
            logo: "https://cdn.pycon.it/sponsors/lamanna.png",
            url: "https://example.org",
          },
        ],
      },
    ]}
  />
);

export const InGrid = () => (
  <Grid cols={12} mdCols={12}>
    <GridColumn colSpan={5} mdColSpan={5}>
      test
    </GridColumn>
    <GridColumn colStart={6} colSpan={6} mdColStart={6} mdColSpan={6}>
      <SponsorsGrid
        tiers={[
          {
            name: "Keystone",
            cols: 1,
            sponsors: [
              {
                name: "Example",
                logo: "https://cdn.pycon.it/sponsors/421478580cba88069f8c12200b032dc1_1.png",
                url: "https://example.org",
              },
            ],
          },
          {
            name: "Gold",
            cols: 2,
            sponsors: [
              {
                name: "Example",
                logo: "https://cdn.pycon.it/sponsors/cloudamqp-by-84codes-original.png",
                url: "https://example.org",
              },
              {
                name: "Example",
                logo: "https://cdn.pycon.it/sponsors/Manninglogo_outline.png",
                url: "https://example.org",
              },
            ],
          },
          {
            name: "Silver",
            cols: 3,
            sponsors: [
              {
                name: "Example",
                logo: "https://cdn.pycon.it/sponsors/lamanna.png",
                url: "https://example.org",
              },
              {
                name: "Example",
                logo: "https://cdn.pycon.it/sponsors/lamanna.png",
                url: "https://example.org",
              },
              {
                name: "Example",
                logo: "https://cdn.pycon.it/sponsors/Manninglogo_outline.png",
                url: "https://example.org",
              },
              {
                name: "Example",
                logo: "https://cdn.pycon.it/sponsors/lamanna.png",
                url: "https://example.org",
              },
              {
                name: "Example",
                logo: "https://cdn.pycon.it/sponsors/lamanna.png",
                url: "https://example.org",
              },
            ],
          },
        ]}
      />
    </GridColumn>
  </Grid>
);
