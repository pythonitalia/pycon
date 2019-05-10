import * as React from 'react';
import { RouteComponentProps } from '@reach/router';

import {
  Schedule as ScheduleType,
  Schedule_conference_schedule,
  ScheduleVariables,
} from './types/Schedule';

import { Query } from 'react-apollo';

import SCHEDULE from './query.graphql';

import * as styles from './style.css';
import { ScheduleTable } from '../../components/schedule-table/index';

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
  let previousItem;
  let currentGroup = 0;

  for (const item of schedule) {
    const start = new Date(item.start);
    const end = new Date(item.end);
    const day = start.getDate();

    /* this does not really work for conferences that span multiple months!!!! */
    /* also it's ugly */
    if (!output.hasOwnProperty(day)) {
      output[day] = {
        year: start.getFullYear(),
        month: start.getMonth(),
        day,
        schedule: {},
      };
      currentGroup = 0;
    }

    if (previousItem) {
      const previousItemStart = new Date(previousItem.end);

      if (previousItemStart.getTime() - end.getTime() > 60 * 60 * 1000) {
        console.log('more than 20 minutes of distance');
        currentGroup++;
        if (!output[day].schedule.hasOwnProperty(currentGroup)) {
          output[day].schedule[currentGroup] = { items: [] };
        }
        output[day].schedule[currentGroup].items.push(item);
      } else {
        console.log('less than 20 minutes of distance');

        if (!output[day].schedule.hasOwnProperty(currentGroup)) {
          output[day].schedule[currentGroup] = { items: [] };
        }

        output[day].schedule[currentGroup].items.push(item);
      }
    }
    // output[day].schedule.push(item);

    previousItem = item;

    console.log(item.title, item.start);
  }

  return output;
};
