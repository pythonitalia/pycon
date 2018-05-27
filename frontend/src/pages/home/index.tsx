import * as React from 'react';
import { Navbar } from 'components/navbar';
import { Button } from 'components/button';
import { Grid, Column } from 'components/grid';
import { Card } from 'components/card';
import { Hero } from 'components/hero';
import { Title, Subtitle } from 'components/typography';

export const HomePage = () => (
  <div>
    <Navbar />

    <Hero
      renderFooter={() => (
        <React.Fragment>
          <Button>Get your Ticket</Button>
          <Button variant="secondary">Propose a talk</Button>
        </React.Fragment>
      )}
    >
      <Title>PyCon 10</Title>
      <Subtitle>Florence, XX XXXX 2019</Subtitle>
      <Subtitle level={2}>Location</Subtitle>
    </Hero>

    <div className="pitch">
      <div>
        <h2>Perché la pycon</h2>

        <p>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Incidunt,
          reprehenderit labore, voluptatem officia velit rerum amet excepturi
          esse, sit ea harum! Aspernatur, earum. Dolor sed commodi non
          laudantium, ipsam veniam?
        </p>
      </div>

      <div>
        <h2>Di cosa parleremo</h2>

        <h3>Data</h3>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Incidunt,
          reprehenderit labore, voluptatem officia velit rerum amet excepturi
          esse, sit ea harum! Aspernatur, earum. Dolor sed commodi non
          laudantium, ipsam veniam?
        </p>

        <h3>Web</h3>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Incidunt,
          reprehenderit labore, voluptatem officia velit rerum amet excepturi
          esse, sit ea harum! Aspernatur, earum. Dolor sed commodi non
          laudantium, ipsam veniam?
        </p>
      </div>
    </div>

    <div className="keynote-speakers">
      <Grid>
        <Column cols={4}>
          <Card>Example</Card>
          <Card>Example</Card>
        </Column>
        <Column cols={4}>
          <Card>Example</Card>
          <Card>Example</Card>
        </Column>
        <Column cols={4}>
          <Card>Example</Card>
          <Card>Example</Card>
        </Column>
      </Grid>

      <Button variant="secondary">See the schedule</Button>
    </div>
  </div>
);
