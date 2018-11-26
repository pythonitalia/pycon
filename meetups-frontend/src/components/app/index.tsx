import * as React from 'react';

import styled from 'styled-components';

import { Router, RouteComponentProps } from '@reach/router';

import {
  Flex,
  Text,
  Icon,
  Box,
  Section,
  Heading,
  Button,
  Image,
  ThemeProvider,
} from '@hackclub/design-system';

import './base.css';
import './typography.css';
import { Hero } from '../hero/index';

import theme from '../../theme';
import Logo from '../logo';

const Chip = (props: any) => <Box w={1} p={5} {...props} />;

const Pre = styled(Text.withComponent('pre'))`
  font-family: ${theme.mono};
`;

const Card = ({ name, color }: { name: string; color: string }) => (
  <Box>
    <Chip name={name} bg={color} />
    <Text fontSize={2} m={0} bold>
      {name}
    </Text>
    <Pre fontSize={0} m={0} color="muted">
      {color}
    </Pre>
  </Box>
);

const Home = (props: RouteComponentProps) => (
  <>
    <Hero
      px={6}
      backgroundImage="https://evway.net/wp-content/uploads/2017/10/Trento.jpg"
    >
      <Logo />

      <Text fontSize={4} align="left">
        Python Roma è un meetup gratuito dedicato a Python.
      </Text>
    </Hero>

    <Flex wrap color="white" bg="base" px={6}>
      <Box width={3 / 4} py={6}>
        <Text fontWeight="bold">Prossimo evento</Text>
        <Text fontSize={6} color="accent">
          16 gennaio 2019
        </Text>
        <Text>19:00 &mdash; 21:30</Text>
        <Text>CLAB, Trento</Text>
      </Box>

      <Flex width={1 / 4} py={4} align="center" justify="flex">
        <Box fontSize={3}>
          <Button bg="accent" color="base" px={5} py={2}>
            Registrati
          </Button>
        </Box>
      </Flex>
    </Flex>

    <Section bg="scale.1" px={6}>
      <Heading.h1 mb={6}>Speakers</Heading.h1>

      <Box>
        <Flex color="white" mb={6}>
          <Box width={300} mr={4}>
            <Image
              width={150}
              alt="TODO"
              src="https://d3iw72m71ie81c.cloudfront.net/gaurav.JPG"
            />
          </Box>
          <Box align="left">
            <Text fontWeight="bold">Joe Noel</Text>
            <Text fontSize={3} color="accent">
              Python 2 is dead
            </Text>
            <Text>
              Lorem ipsum dolor, sit amet consectetur adipisicing elit. Corrupti
              facilis, cupiditate, architecto quam ut ducimus eveniet rem nBoxla
              voluptates mollitia vitae eos, consectetur ullam totam
              reprehenderit accusamus similique accusantium fugit.
            </Text>
          </Box>
        </Flex>
        <Flex color="white" mb={6}>
          <Box width={300} mr={4}>
            <Image
              alt="TODO"
              width={150}
              src="https://d3iw72m71ie81c.cloudfront.net/gaurav.JPG"
            />
          </Box>
          <Box align="left">
            <Text fontWeight="bold">Joe Noel</Text>
            <Text fontSize={3} color="accent">
              Python 2 is dead
            </Text>
            <Text>
              Lorem ipsum dolor, sit amet consectetur adipisicing elit. Corrupti
              facilis, cupiditate, architecto quam ut ducimus eveniet rem nulla
              voluptates mollitia vitae eos, consectetur ullam totam
              reprehenderit accusamus similique accusantium fugit.
            </Text>
          </Box>
        </Flex>
      </Box>
    </Section>

    <Section bg="accent">
      <Heading.h1>Mailing list</Heading.h1>

      <Button mt={6}>Registrati</Button>
    </Section>

    <Section bg="accentScale.1">
      <Heading.h1>Call for Speakers</Heading.h1>
      <Text>Ti va di presentare un talk a Python Roma?</Text>

      <Button mt={6}>Compila il form</Button>
    </Section>

    <Section bg="smoke">
      <Text color="dark">Python Roma</Text>
    </Section>

    <Heading.h1>Colors</Heading.h1>

    <pre>{JSON.stringify(theme.colors, null, 4)}</pre>

    {Object.keys(theme.colors).map(key => (
      <Flex wrap>
        {' '}
        {Array.isArray(theme.colors[key]) ? (
          theme.colors[key].map((e, i) => (
            <Card name={`${key}.${i}`} color={`${key}.${i}`} />
          ))
        ) : (
          <Card name={key} color={key} />
        )}
      </Flex>
    ))}
  </>
);
const Dash = (props: RouteComponentProps) => <div>Dash</div>;

export const App = () => (
  <ThemeProvider webfonts theme={theme}>
    <Router>
      <Home path="/" />
      <Dash path="dashboard" />
    </Router>
  </ThemeProvider>
);
