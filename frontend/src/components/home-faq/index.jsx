"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const fannypack_1 = require("fannypack");
const grigliata_1 = require("grigliata");
const styled_components_1 = __importDefault(require("styled-components"));
const spacing_1 = require("../../config/spacing");
const section_title_1 = require("../section-title");
const Wrapper = styled_components_1.default.div `
  margin-top: 2rem;
`;
exports.Faq = () => {
    const PADDING_RIGHT = {
        mobile: 0,
        tabletPortrait: 3,
        tabletLandscape: 3,
        desktop: 3,
    };
    return (<Wrapper>
      <grigliata_1.Row paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
        <grigliata_1.Column columnWidth={{
        mobile: 12,
        tabletPortrait: 12,
        tabletLandscape: 12,
        desktop: 12,
    }}>
          <section_title_1.SectionTitle>FAQ</section_title_1.SectionTitle>
        </grigliata_1.Column>
      </grigliata_1.Row>
      <grigliata_1.Row marginTop={{
        desktop: -4,
        tabletLandscape: -3,
        tabletPortrait: 0,
        mobile: 0,
    }} paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
        <grigliata_1.Column paddingRight={PADDING_RIGHT} columnWidth={{
        mobile: 12,
        tabletPortrait: 6,
        tabletLandscape: 6,
        desktop: 6,
    }}>
          <fannypack_1.Heading use="h3">How can I contribute?</fannypack_1.Heading>
          <fannypack_1.Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </fannypack_1.Text>
        </grigliata_1.Column>
        <grigliata_1.Column paddingRight={PADDING_RIGHT} columnWidth={{
        mobile: 12,
        tabletPortrait: 6,
        tabletLandscape: 6,
        desktop: 6,
    }}>
          <fannypack_1.Heading use="h3">Where is the venue?</fannypack_1.Heading>
          <fannypack_1.Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </fannypack_1.Text>
        </grigliata_1.Column>
        <grigliata_1.Column paddingRight={PADDING_RIGHT} columnWidth={{
        mobile: 12,
        tabletPortrait: 6,
        tabletLandscape: 6,
        desktop: 6,
    }}>
          <fannypack_1.Heading use="h3">When will the event take place?</fannypack_1.Heading>
          <fannypack_1.Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </fannypack_1.Text>
        </grigliata_1.Column>
        <grigliata_1.Column paddingRight={PADDING_RIGHT} columnWidth={{
        mobile: 12,
        tabletPortrait: 6,
        tabletLandscape: 6,
        desktop: 6,
    }}>
          <fannypack_1.Heading use="h3">Where is the venue?</fannypack_1.Heading>
          <fannypack_1.Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </fannypack_1.Text>
        </grigliata_1.Column>
      </grigliata_1.Row>
    </Wrapper>);
};
