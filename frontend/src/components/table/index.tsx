import * as React from 'react';

import * as styles from './style.css';

export type ColumnHeader = {
  label: string;
  accessor: string;
};

type Props = {
  columns: ColumnHeader[];
  data: object[];
};

export class Table extends React.Component<Props, {}> {
  public render() {
    const { columns } = this.props;
    const countColumns = columns.length;

    return (
      <div className={styles.table}>
        <div className={`${styles.head} ${styles.row}`}>
          <span className={styles.checkbox} />
          {columns.map(c => (
            <span
              style={{ flexBasis: `calc(95% / ${countColumns})` }}
              key={c.label}
            >
              {c.label}
            </span>
          ))}
        </div>
        <div className={styles.body}>{this.renderBody()}</div>
      </div>
    );
  }

  private renderBody() {
    const { columns, data } = this.props;
    const countColumns = columns.length;

    return data.map((item: any, i) => (
      <div className={styles.row} key={i}>
        <span className={styles.checkbox} />
        {columns.map(column => (
          <span
            style={{ flexBasis: `calc(95% / ${countColumns})` }}
            key={column.label}
          >
            {item[column.accessor]}
          </span>
        ))}
      </div>
    ));
  }
}
