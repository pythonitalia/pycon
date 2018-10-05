import * as React from 'react';

import * as styles from './style.css';

export type ColumnHeader<T> = {
  label: string;
  accessor: (<TReturn>(object: T) => TReturn) | string;
};


type Props<T> = {
  columns: Array<ColumnHeader<T>>;
  data: T[];
};

export class Table<T> extends React.Component<Props<T>, {}> {

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

    return data.map((item: T, i) => (
      <tr key={i}>
        <td className={styles.checkbox} />
        {columns.map(column => {
          const value =
            typeof column.accessor === 'function'
              ? column.accessor(item)
              : item[column.accessor as keyof(T)];

          return <td key={column.label}>{value}</td>;
        })}
      </tr>
    ));
  }
}
