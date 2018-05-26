import React from 'react';

import TopAppBar from '../../vendor/react-material/top-app-bar';
import MaterialIcon from '../../vendor/react-material/material-icon';

export class Navbar extends React.Component<{}, {}> {
  render() {
    return (
      <TopAppBar
        title="PyCon 10"
        navigationIcon={<MaterialIcon icon="menu" />}
        actionItems={[<MaterialIcon key="item" icon="bookmark" />]}
      >
        a
      </TopAppBar>
    );
  }
}
