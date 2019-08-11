"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
exports.useToggle = (defaultValue) => {
    const [value, setValue] = react_1.useState(defaultValue), toggle = () => {
        setValue(!value);
    };
    return [value, toggle];
};
