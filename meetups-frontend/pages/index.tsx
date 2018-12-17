import * as React from 'react';
import { Hero } from '../components/hero';
import { Logo } from '../components/logo';

import {
  Flex,
  Text,
  Box,
  Section,
  Heading,
  Container,
  Button,
  Image,
} from '@hackclub/design-system';
import { AppWrapper } from '../components/app-wrapper';

export default () => (
  <AppWrapper>
    <Hero backgroundImage="https://source.unsplash.com/1600x900/?rome">
      <Logo />

      <Text fontSize={4} align="left">
        Python Roma è un meetup gratuito dedicato a Python.
      </Text>
    </Hero>

    <Flex color="white" bg="primary" px={2}>
      <Container style={{ width: '100%' }}>
        <Flex wrap color="white" bg="primary">
          <Box py={[5, 6]} mr="auto">
            <Text fontWeight="bold">Prossimo evento</Text>
            <Text fontSize={[3, 5, 6]} color="accent">
              16 gennaio 2019
            </Text>
            <Text>19:00 &mdash; 21:30</Text>
            <Text>CLAB, Trento</Text>
          </Box>

          <Flex py={4} align="center" justify="flex">
            <Box fontSize={3}>
              <Button bg="accent" color="primary" px={5} py={2}>
                Registrati
              </Button>
            </Box>
          </Flex>
        </Flex>
      </Container>
    </Flex>

    <Section bg="scale.1">
      <Container>
        <Heading.h1 mb={6}>Speakers</Heading.h1>

        <Box mb={4}>
          <Flex color="white" mb={3}>
            <Box width={100} mr={3}>
              <Image
                width={100}
                alt="TODO"
                src="https://d3iw72m71ie81c.cloudfront.net/gaurav.JPG"
              />
            </Box>
            <Box align="left">
              <Text fontSize={[1]} fontWeight="bold">
                Joe Noel
              </Text>
              <Text fontSize={[3, 6]} color="accent">
                Python 2 is dead
              </Text>
            </Box>
          </Flex>
          <Text align="left">
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Corrupti
            facilis, cupiditate, architecto quam ut ducimus eveniet rem nBoxla
            voluptates mollitia vitae eos, consectetur ullam totam reprehenderit
            accusamus similique accusantium fugit.
          </Text>
        </Box>

        <Box mb={4}>
          <Flex color="white" mb={3}>
            <Box width={100} mr={3}>
              <Image
                width={100}
                alt="TODO"
                src="https://d3iw72m71ie81c.cloudfront.net/gaurav.JPG"
              />
            </Box>
            <Box align="left">
              <Text fontSize={[1]} fontWeight="bold">
                Joe Noel
              </Text>
              <Text fontSize={[3, 6]} color="accent">
                Python 2 is dead
              </Text>
            </Box>
          </Flex>
          <Text align="left">
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Corrupti
            facilis, cupiditate, architecto quam ut ducimus eveniet rem nBoxla
            voluptates mollitia vitae eos, consectetur ullam totam reprehenderit
            accusamus similique accusantium fugit.
          </Text>
        </Box>
      </Container>
    </Section>

    <Section bg="accent">
      <Container>
        <Heading.h1>Mailing list</Heading.h1>

        <Button mt={6}>Registrati</Button>
      </Container>
    </Section>

    <Section bg="accentScale.1">
      <Container>
        <Heading.h1>Call for Speakers</Heading.h1>
        <Text>Ti va di presentare un talk a Python Roma?</Text>

        <Button mt={6}>Compila il form</Button>
      </Container>
    </Section>

    <Section bg="white">
      <Container>
        <Text color="black">Python Roma</Text>
      </Container>
    </Section>
  </AppWrapper>
);
