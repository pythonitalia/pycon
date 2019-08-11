"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const styled_components_1 = __importDefault(require("styled-components"));
const section_title_1 = require("../section-title");
exports.ArticleTitle = styled_components_1.default(section_title_1.SectionTitle) `
  color: ${props => props.theme.palette.white};
`;
