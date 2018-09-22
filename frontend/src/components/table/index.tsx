import * as React from 'react';

import * as styles from './style.css';

interface Props {
  columns: string[];
  data: object[];
}

export class Table extends React.Component<Props, {}> {
  public render() {
    const { columns, data } = this.props;
    return (
      <table className={styles.table} cellSpacing={0}>
        <thead>
          <tr>
            <th>Select</th>
            {columns.map(c => (
              <th>{c}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map(() => (
            <tr>
              <td />
              <td>Patrick Arminio</td>
              <td>Attivo</td>
              <td>20 aprile 2019</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
}
