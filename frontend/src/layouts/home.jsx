"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const fannypack_1 = require("fannypack");
const styled_components_1 = __importDefault(require("styled-components"));
const footer_1 = require("../components/footer");
const topbar_1 = require("../components/topbar");
const theme_1 = require("../config/theme");
const Wrapper = styled_components_1.default.div `
  padding-top: 80px;
`;
exports.HomeLayout = (props) => (<fannypack_1.ThemeProvider theme={theme_1.theme}>
    <Wrapper>
      <topbar_1.Topbar />
      <div>{props.children}</div>
      <footer_1.Footer />
    </Wrapper>
  </fannypack_1.ThemeProvider>);
