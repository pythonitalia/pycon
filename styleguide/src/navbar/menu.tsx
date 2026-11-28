import React from "react";
import { Container } from "../container";
import { Heading } from "../heading";
import { Link } from "../link";
import { Separator } from "../separator";
import { Text } from "../text";
import type { Link as LinkType } from "./types";

export const Menu = ({
  mainLinks,
  secondaryLinks,
  bottomBarLink,
}: {
  mainLinks: LinkType[];
  secondaryLinks: LinkType[];
  bottomBarLink?: LinkType;
}) => {
  const mainLinksSplit = splitLinks(mainLinks, 2);
  const secondaryLinksSplit = splitLinks(secondaryLinks, 4);

  return (
    <div>
      {mainLinks.length > 0 && (
        <>
          <Separator />
          <Container className="py-8 lg:py-20">
            <div className="grid grid-cols-1 gap-4 lg:gap-14 lg:grid-cols-2">
              {mainLinksSplit
                .filter((split) => split.length > 0)
                .map((split, index) => (
                  <ul
                    className="grid grid-cols-1 content-start gap-4 lg:gap-6"
                    key={index}
                  >
                    {split.map(({ text, link }) => (
                      <li key={`${text}${link}`}>
                        <Link hoverColor="caramel" href={link}>
                          <Heading color="none" size="display2">
                            {text}
                          </Heading>
                        </Link>
                      </li>
                    ))}
                  </ul>
                ))}
            </div>
          </Container>
        </>
      )}
      {secondaryLinks.length > 0 && (
        <>
          <Separator />
          <Container className="py-8 lg:py-10">
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 lg:gap-14">
              {secondaryLinksSplit
                .filter((split) => split.length > 0)
                .map((secondaryLinks, index) => (
                  <ul
                    key={index}
                    className="grid grid-cols-1 gap-4 content-start"
                  >
                    {secondaryLinks.map(({ link, text }) => (
                      <li key={`${text}${link}`}>
                        <Link hoverColor="caramel" href={link}>
                          <Heading color="none" size={4}>
                            {text}
                          </Heading>
                        </Link>
                      </li>
                    ))}
                  </ul>
                ))}
            </div>
          </Container>
        </>
      )}
      {bottomBarLink && (
        <>
          <Separator />
          <Container className="py-4 lg:py-10 uppercase">
            <Link hoverColor="caramel" href={bottomBarLink.link}>
              <Text size="label3" color="none" weight="strong">
                {bottomBarLink.text}
              </Text>
            </Link>
          </Container>
        </>
      )}
    </div>
  );
};

function splitLinks<T>(links: T[], cols: number): T[][] {
  const slices: T[][] = [];
  const splitPoint = Math.ceil(links.length / cols);

  for (let i = 0; i < cols; i++) {
    slices.push(links.slice(i * splitPoint, (i + 1) * splitPoint));
  }

  return slices;
}
