import * as React from 'react';
import { Navbar } from 'components/navbar';

export class HomePage extends React.Component {
  render() {
    return (
      <div className="App">
        <Navbar />
        <p className="App-intro">
          To get started, edit <code>src/App.tsx</code> and save to reload.
        </p>
      </div>
    );
  }
}
