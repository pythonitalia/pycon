import React from "react";

import { Column } from "fannypack";
import styled from "styled-components";
import { ResponsiveProps, responsiveSpacing } from "../columns";

export type CustomColumnsType = ResponsiveProps;
export const BaseCustomColumn = Column as React.SFC<CustomColumnsType>;

export const CustomColumns = styled(BaseCustomColumn)`
  ${props => responsiveSpacing(props)}
`;
