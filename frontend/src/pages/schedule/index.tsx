import { RouteComponentProps } from '@reach/router';
import * as React from 'react';
import { Query } from 'react-apollo';
import { ScheduleTable } from '../../components/schedule-table/index';
import SCHEDULE from './query.graphql';
import * as styles from './style.css';
import {
  Schedule as ScheduleType,
  ScheduleVariables,
  Schedule_conference_schedule,
} from './types/Schedule';

export const monthIndexToName = [
  'Gennaio',
  'Febbraio',
  'Marzo',
  'Aprile',
  'Maggio',
  'Giugno',
  'Luglio',
  'Agosto',
  'Settembre',
  'Ottobre',
  'Novembre',
  'Dicembre',
];

type ScheduleGroup = {
  items: Schedule_conference_schedule[];
};

type ScheduleGroupContainer = {
  [index: string]: ScheduleGroup;
};

export type ParsedSchedule = {
  year: number;
  month: number;
  day: number;
  schedule: ScheduleGroupContainer;
};

type ParsedScheduleContainer = {
  [index: string]: ParsedSchedule;
};

export const Schedule = (props: RouteComponentProps) => {
  return (
    <Query<ScheduleType, ScheduleVariables>
      query={SCHEDULE}
      variables={{ conf: 'pycon9' }}
    >
      {({ loading, error, data }) => {
        if (loading) {
          return <div>Hang on...</div>;
        }

        if (error) {
          return <div>Something went wrong</div>;
        }

        const schedule = parseSchedule(data.conference.schedule);
        const days = Object.keys(schedule);
        const activeDay = schedule[days[1]];

        return (
          <div className={styles.schedule}>
            <h1 className={styles.title}>Schedule</h1>
            <ul className={styles.days}>
              {days.map((day, index) => (
                <li
                  className={`${styles.day} ${
                    index === 0 ? styles.activeDay : ''
                  }`}
                >
                  {monthIndexToName[schedule[day].month]} {schedule[day].day}
                </li>
              ))}
            </ul>
            <ScheduleTable schedule={activeDay} />
          </div>
        );
      }}
    </Query>
  );
};

const parseSchedule = (
  schedule: Schedule_conference_schedule[],
): ParsedScheduleContainer => {
  const output: ParsedScheduleContainer = {};
  /* removed test code */
  return output;
};
