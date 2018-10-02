import * as React from 'react';

import * as styles from './style.css';

export type ColumnHeader = {
  label: string;
  accessor: ((object: any) => any) | string;
};

type Props = {
  columns: ColumnHeader[];
  data: object[];
};

export class Table extends React.Component<Props, {}> {
  public render() {
    const { columns } = this.props;

    return (
      <table className={styles.table}>
        <thead>
          <tr>
            <th className={styles.checkbox} />
            {columns.map(c => (
              <th key={c.label}>{c.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>{this.renderBody()}</tbody>
      </table>
    );
  }

  private renderBody() {
    const { columns, data } = this.props;

    return data.map((item: any, i) => (
      <tr key={i}>
        <td className={styles.checkbox} />
        {columns.map(column => {
          const value =
            typeof column.accessor === 'function'
              ? column.accessor(item)
              : item[column.accessor];

          return <td key={column.label}>{value}</td>;
        })}
      </tr>
    ));
  }
}
