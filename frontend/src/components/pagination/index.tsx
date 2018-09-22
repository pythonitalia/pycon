import * as React from 'react';
import classnames from 'classnames';

import { range } from '../../utils';

import * as styles from './style.css';

type Props = {
  currentPage: number;
  totalItems: number;
  itemsPerPage: number;
  onPageChange?: (nextPage: number) => void;
};

export class Pagination extends React.Component<Props, {}> {
  private changePage(nextPage: number, e: React.MouseEvent<HTMLSpanElement>) {
    if (nextPage < 0 || nextPage >= this.getTotalPages()) {
      return;
    }

    if (this.props.onPageChange) {
      this.props.onPageChange(nextPage);
    }
  }

  private getTotalPages() {
    const { totalItems, itemsPerPage } = this.props;
    return Math.ceil(totalItems / itemsPerPage);
  }

  public render() {
    const { currentPage } = this.props;
    const totalPages = this.getTotalPages();

    if (totalPages === 1) {
      return null;
    }

    const prevClasses = classnames(styles.action, {
      [styles.disabled]: currentPage === 0,
    });

    const nextClasses = classnames(styles.action, {
      [styles.disabled]: currentPage >= totalPages - 1,
    });

    return (
      <div className={styles.pagination}>
        <span
          className={prevClasses}
          onClick={this.changePage.bind(this, currentPage - 1)}
        >
          Prev
        </span>
        {range(1, totalPages + 1).map(p => (
          <span
            className={classnames(styles.number, {
              [styles.activePage]: p - 1 === currentPage,
            })}
            onClick={this.changePage.bind(this, p - 1)}
            key={p}
          >
            {p}
          </span>
        ))}
        <span
          className={nextClasses}
          onClick={this.changePage.bind(this, currentPage + 1)}
        >
          Next
        </span>
      </div>
    );
  }
}
