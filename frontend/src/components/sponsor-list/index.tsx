import React from "react";

import { Heading, List } from "fannypack";
import Img, { GatsbyImageProps } from "gatsby-image";
import styled from "styled-components";
import { STANDARD_CUSTOM_COLUMNS_PADDING } from "../../config/spacing";
import { CustomColumn } from "../column";
import { CustomColumns } from "../columns";
import { SectionTitle } from "../section-title";

const Wrapper = styled.div`
li {
  width: 100%;
  max-width: 250px;
}
`;

type Sponsor = Array<{name: string, logo: GatsbyImageProps, category: string, link: string}>;

type SponsorListProps = {
  sponsors: Sponsor;
};

export const SponsorList: React.SFC<SponsorListProps> = props => {

  const grouppedSponsors = new Map<string, Sponsor>();

  for (const sponsor of props.sponsors) {
    if (grouppedSponsors.has(sponsor.category)) {
      const categorizedSponsors = grouppedSponsors.get(sponsor.category);
      if (!categorizedSponsors) {
        continue;
      }
      categorizedSponsors.push(sponsor);
    } else {
      grouppedSponsors.set(sponsor.category, [sponsor]);
    }
  }

  const sponsorsItems = Array.from(grouppedSponsors.entries()).map((value, categoryIndex) => {
    const category = value[0];
    const sponsors = value[1];
    const listItems = sponsors.map((sponsor, sponsorIndex) => (
      <List.Item key={sponsorIndex}>
        <Img {...sponsor.logo} alt={sponsor.name}/>
      </List.Item>
      )
    );
    return (
      <div key={categoryIndex}>
        <CustomColumns
          marginTop={categoryIndex === 0 ? { desktop: -4, tablet: -4, mobile: -1 } : {desktop: 0, tablet: 0, mobile: 0}}
          paddingLeft={STANDARD_CUSTOM_COLUMNS_PADDING}
          paddingRight={STANDARD_CUSTOM_COLUMNS_PADDING}
        >
          <CustomColumn
            paddingRight={{ desktop: 3, tablet: 2, mobile: 0 }}
            spreadMobile={12}
            spread={6}
            spreadDesktop={12}
          >
            <Heading use="h5">{category}</Heading>
            <List isHorizontal={true}>
              {listItems}
            </List>
          </CustomColumn>
        </CustomColumns>
      </div>
      );
    }
  );
  return (
    <Wrapper>
      <CustomColumns
        paddingLeft={STANDARD_CUSTOM_COLUMNS_PADDING}
        paddingRight={STANDARD_CUSTOM_COLUMNS_PADDING}
      >
        <CustomColumn>
          <SectionTitle>Sponsors</SectionTitle>
          </CustomColumn>
      </CustomColumns>
      { sponsorsItems }
    </Wrapper>
  );
};
