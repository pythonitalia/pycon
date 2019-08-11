"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const fannypack_1 = require("fannypack");
exports.Button = (props) => (<fannypack_1.Button {...props}>{props.children}</fannypack_1.Button>);
