import * as React from 'react';
import { ParsedSchedule, monthIndexToName } from '../../pages/schedule/index';
import { ScheduleItemType } from '../../types/global';
import { Schedule_conference_schedule } from '../../pages/schedule/types/Schedule';

import * as styles from './style.css';

type Props = {
  schedule: ParsedSchedule;
};

export const ScheduleTable = (props: Props) => {
  const schedule = props.schedule;
  return (
    <div>
      <h2>
        {monthIndexToName[schedule.month]} {schedule.day}
      </h2>
      {Object.keys(schedule.schedule).map(groupId => {
        const group = schedule.schedule[groupId];
        const firstItem = group.items[0];
        const dateFirstItem = new Date(firstItem.start);

        return (
          <div>
            <h3>Group #{groupId}</h3>
            <div className={styles.groupContainer}>
              <h4 className={styles.groupTitle}>
                {dateFirstItem.getHours()}:{dateFirstItem.getMinutes()}
              </h4>
              {group.items.map(item => (
                <ScheduleItem item={item} />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};

type ScheduleItemProps = {
  item: Schedule_conference_schedule;
};

const ScheduleItem = (props: ScheduleItemProps) => {
  const item = props.item;
  const title =
    item.type === ScheduleItemType.CUSTOM ? item.title : item.submission.title;
  const description =
    item.type === ScheduleItemType.CUSTOM
      ? item.description
      : item.submission.abstract;
  return (
    <div className={styles.scheduleItem}>
      <h5>{title}</h5>
      <p dangerouslySetInnerHTML={{ __html: description }} />
      <ul className={styles.rooms}>
        {item.rooms.map(room => (
          <li key={room.name}>{room.name}</li>
        ))}
      </ul>
    </div>
  );
};
