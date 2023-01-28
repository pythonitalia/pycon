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
        sponsors: [
          {
            name: "Google",
            logo: "https://cdn.pycon.it/sponsors/cloudamqp-by-84codes-original.png",
            url: "https://google.com",
          },
          {
            name: "Facebook",
            logo: "https://cdn.pycon.it/sponsors/fiscozen.png",
            url: "https://facebook.com",
          },
        ],
      },
      {
        name: "Gold",
        sponsors: [
          {
            name: "Google",
            logo: "https://cdn.pycon.it/sponsors/cloudamqp-by-84codes-original.png",
            url: "https://google.com",
          },
          {
            name: "Facebook",
            logo: "https://cdn.pycon.it/sponsors/Manninglogo_outline.png",
            url: "https://facebook.com",
          },
        ],
      },
      {
        name: "Silver",
        sponsors: [
          {
            name: "Google",
            logo: "https://cdn.pycon.it/sponsors/lamanna.png",
            url: "https://google.com",
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
            cols: 2,
            sponsors: [
              {
                name: "Google",
                logo: "https://cdn.pycon.it/sponsors/cloudamqp-by-84codes-original.png",
                url: "https://google.com",
              },
              {
                name: "Facebook",
                logo: "https://cdn.pycon.it/sponsors/fiscozen.png",
                url: "https://facebook.com",
              },
            ],
          },
          {
            name: "Gold",
            cols: 2,
            sponsors: [
              {
                name: "Google",
                logo: "https://cdn.pycon.it/sponsors/cloudamqp-by-84codes-original.png",
                url: "https://google.com",
              },
              {
                name: "Facebook",
                logo: "https://cdn.pycon.it/sponsors/Manninglogo_outline.png",
                url: "https://facebook.com",
              },
            ],
          },
          {
            name: "Silver",
            cols: 3,
            sponsors: [
              {
                name: "Google",
                logo: "https://cdn.pycon.it/sponsors/lamanna.png",
                url: "https://google.com",
              },
              {
                name: "Google",
                logo: "https://cdn.pycon.it/sponsors/lamanna.png",
                url: "https://google.com",
              },
              {
                name: "Google",
                logo: "https://cdn.pycon.it/sponsors/Manninglogo_outline.png",
                url: "https://google.com",
              },
              {
                name: "Google",
                logo: "https://cdn.pycon.it/sponsors/lamanna.png",
                url: "https://google.com",
              },
              {
                name: "Google",
                logo: "https://cdn.pycon.it/sponsors/lamanna.png",
                url: "https://google.com",
              },
            ],
          },
        ]}
      />
    </GridColumn>
  </Grid>
);
