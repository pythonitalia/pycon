"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const fannypack_1 = require("fannypack");
const gatsby_1 = require("gatsby");
const grigliata_1 = require("grigliata");
const spacing_1 = require("../../config/spacing");
const button_1 = require("../button");
const constants_1 = require("./constants");
const links_wrapper_1 = require("./links-wrapper");
const map_wrapper_1 = require("./map-wrapper");
const wrapper_1 = require("./wrapper");
exports.Footer = () => {
    const MARGIN_TOP_ROW = {
        mobile: 1,
        tabletPortrait: 5,
        tabletLandscape: 5,
        desktop: 5,
    };
    return (<wrapper_1.Wrapper>
      <grigliata_1.Row paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING} paddingTop={MARGIN_TOP_ROW}>
        <grigliata_1.Column paddingRight={{
        mobile: 0,
        tabletPortrait: 3,
        tabletLandscape: 3,
        desktop: 3,
    }} columnWidth={{
        mobile: 12,
        tabletPortrait: 6,
        tabletLandscape: 6,
        desktop: 6,
    }}>
          <fannypack_1.Heading use="h3">keep up to date</fannypack_1.Heading>
          <fannypack_1.Text>
            Stay in the loop, sign up for email updates about events, news and
            offers.
          </fannypack_1.Text>
          <div>
            <form action="">
              <grigliata_1.Row marginLeft={{
        mobile: -0.5,
        tabletPortrait: -0.5,
        tabletLandscape: -0.5,
        desktop: -0.5,
    }} marginRight={{
        mobile: -0.5,
        tabletPortrait: -0.5,
        tabletLandscape: -0.5,
        desktop: -0.5,
    }} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
                <grigliata_1.Column columnWidth={{
        mobile: 12,
        tabletPortrait: 9,
        tabletLandscape: 9,
        desktop: 9,
    }}>
                  <fannypack_1.Input placeholder="Email" type="email"/>
                </grigliata_1.Column>
                <grigliata_1.Column columnWidth={{
        mobile: 12,
        tabletPortrait: 3,
        tabletLandscape: 3,
        desktop: 3,
    }}>
                  <button_1.Button margin="0" palette={"white"}>
                    Sign up
                  </button_1.Button>
                </grigliata_1.Column>
              </grigliata_1.Row>
            </form>
          </div>
        </grigliata_1.Column>
        <grigliata_1.Column paddingRight={{
        mobile: 0,
        tabletPortrait: 3,
        tabletLandscape: 3,
        desktop: 3,
    }} columnWidth={{
        mobile: 12,
        tabletPortrait: 6,
        tabletLandscape: 6,
        desktop: 6,
    }}>
          <fannypack_1.Heading use="h3">donations</fannypack_1.Heading>
          <div>
            <fannypack_1.Text>
              Stay in the loop, sign up for email updates about events, news and
              offers.
            </fannypack_1.Text>
          </div>

          <button_1.Button marginTop="major-2" palette={"white"}>
            Donate now
          </button_1.Button>
        </grigliata_1.Column>
      </grigliata_1.Row>

      <grigliata_1.Row marginTop={MARGIN_TOP_ROW}>
        <map_wrapper_1.MapWrapper style={{ width: "100%" }}>
          <a href="https://www.google.com/maps/place/hotel+mediterraneo+firenze/">
            <img src={constants_1.GOOGLE_MAPS_URL} alt="Google Map of hotel Mediterraneo Firenze"/>
          </a>
        </map_wrapper_1.MapWrapper>
      </grigliata_1.Row>

      <grigliata_1.Row paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING} marginTop={MARGIN_TOP_ROW} marginBottom={MARGIN_TOP_ROW}>
        {[1, 2, 3, 4].map((o, i) => (<grigliata_1.Column key={i} columnWidth={{
        mobile: 12,
        tabletPortrait: 6,
        tabletLandscape: 3,
        desktop: 3,
    }}>
            <fannypack_1.Heading use="h4">our venues</fannypack_1.Heading>
            <links_wrapper_1.LinksWrapper>
              <gatsby_1.Link to="/">Link</gatsby_1.Link>
              <gatsby_1.Link to="/">Link</gatsby_1.Link>
              <gatsby_1.Link to="/">Link</gatsby_1.Link>
            </links_wrapper_1.LinksWrapper>
          </grigliata_1.Column>))}
      </grigliata_1.Row>
    </wrapper_1.Wrapper>);
};
