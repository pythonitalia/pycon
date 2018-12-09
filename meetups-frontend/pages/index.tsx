import * as React from 'react';
import { Hero } from '../components/hero';
import { Logo } from '../components/logo';

import {
  Flex,
  Text,
  Box,
  Section,
  Heading,
  Button,
  Image,
} from '@hackclub/design-system';
import { AppWrapper } from '../components/app-wrapper';

export default () => (
  <AppWrapper>
    <Hero
      px={6}
      backgroundImage="https://evway.net/wp-content/uploads/2017/10/Trento.jpg"
    >
      <Logo />

      <Text fontSize={4} align="left">
        Python Roma è un meetup gratuito dedicato a Python.
      </Text>
    </Hero>

    <Flex wrap color="white" bg="primary" px={6}>
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
          <Button bg="accent" color="primary" px={5} py={2}>
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

    <Section bg="white">
      <Text color="black">Python Roma</Text>
    </Section>
  </AppWrapper>
);
