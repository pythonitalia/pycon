import React from 'react';

import styled from '../../styled';

import TopAppBar from '../../vendor/react-material/top-app-bar';
import MaterialIcon from '../../vendor/react-material/material-icon';

const Wrapper = styled.div`
  position: relative;
  z-index: 10;
`;

export class Navbar extends React.Component<{}, {}> {
  render() {
    return (
      <Wrapper>
        <TopAppBar
          title="PyCon 10"
          navigationIcon={<MaterialIcon icon="menu" />}
          actionItems={[<MaterialIcon key="item" icon="bookmark" />]}
          style={{
            position: 'relative',
            zIndex: 10,
          }}
        />
      </Wrapper>
    );
  }
}
