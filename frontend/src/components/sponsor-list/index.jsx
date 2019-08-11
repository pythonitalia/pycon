"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const fannypack_1 = require("fannypack");
const gatsby_image_1 = __importDefault(require("gatsby-image"));
const grigliata_1 = require("grigliata");
const styled_components_1 = __importDefault(require("styled-components"));
const spacing_1 = require("../../config/spacing");
const section_title_1 = require("../section-title");
const Wrapper = styled_components_1.default.div ``;
const MARGIN_NEGATIVE_COLUMN = {
    mobile: -0.5,
    tabletPortrait: -0.5,
    tabletLandscape: -0.5,
    desktop: -0.5,
}, FULL_WIDTH_COLUMN = {
    mobile: 12,
    tabletPortrait: 12,
    tabletLandscape: 12,
    desktop: 12,
};
exports.SponsorList = props => (<Wrapper>
    <grigliata_1.Row paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
      <grigliata_1.Column>
        <section_title_1.SectionTitle>Sponsors</section_title_1.SectionTitle>
      </grigliata_1.Column>
    </grigliata_1.Row>
    {props.sponsors.map((o, i) => (<grigliata_1.Row key={i} marginTop={i === 0
    ? {
        mobile: 1,
        tabletPortrait: -1,
        tabletLandscape: -3,
        desktop: -4,
    }
    : {
        mobile: 1,
        tabletPortrait: 1,
        tabletLandscape: 2,
        desktop: 2,
    }} paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
        <grigliata_1.Column columnWidth={FULL_WIDTH_COLUMN}>
          <fannypack_1.Heading use="h5">{o.category}</fannypack_1.Heading>
        </grigliata_1.Column>
        <grigliata_1.Column columnWidth={FULL_WIDTH_COLUMN}>
          <grigliata_1.Row marginLeft={MARGIN_NEGATIVE_COLUMN} marginRight={MARGIN_NEGATIVE_COLUMN}>
            {o.logos.map((sponsor, logosKey) => (<grigliata_1.Column key={logosKey} columnWidth={{
    mobile: 12,
    tabletPortrait: 4,
    tabletLandscape: 3,
    desktop: 3,
}}>
                <a href={sponsor.link}>
                  <gatsby_image_1.default {...sponsor.logo} alt={sponsor.name}/>
                </a>
              </grigliata_1.Column>))}
          </grigliata_1.Row>
        </grigliata_1.Column>
      </grigliata_1.Row>))}
  </Wrapper>);
