import React from "react";

import { Column, LocalColumnProps } from "fannypack";
import styled from "styled-components";
import { ResponsiveProps, responsiveSpacing } from "../columns";

export type CustomColumnsType = ResponsiveProps & LocalColumnProps;

export const BaseCustomColumn = Column as React.SFC<CustomColumnsType>;

export const CustomColumn = styled(BaseCustomColumn)`
  ${props => responsiveSpacing(props)}
`;
