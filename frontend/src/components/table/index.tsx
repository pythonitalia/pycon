import * as React from 'react';

import classnames from 'classnames';

import * as styles from './style.css';

export type ColumnHeader<T> = {
  label: string;
  accessor: ((object: T) => string) | string;
};

type Props<T> = {
  columns: Array<ColumnHeader<T>>;
  data: T[];
  onRowClick?: (item: T, e: React.MouseEvent<HTMLTableRowElement>) => void;
};

export class Table<T> extends React.Component<Props<T>, {}> {
  private onRowClick(item: T, e: React.MouseEvent<HTMLTableRowElement>) {
    e.preventDefault();

    if (this.props.onRowClick) {
      this.props.onRowClick(item, e);
    }
  }

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
    const { columns, data, onRowClick } = this.props;

    return data.map((item: T, i) => (
      <tr
        onClick={this.onRowClick.bind(this, item)}
        key={i}
        className={classnames({
          [styles.clickable]: onRowClick !== null,
        })}
      >
        <td className={styles.checkbox} />
        {columns.map(column => {
          const value =
            typeof column.accessor === 'function'
              ? column.accessor(item)
              : item[column.accessor as keyof (T)];

          return <td key={column.label}>{value}</td>;
        })}
      </tr>
    ));
  }
}
