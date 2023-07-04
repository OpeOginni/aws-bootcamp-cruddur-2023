import "./Replies.css";

import ActivityItem from "./ActivityItem";

export default function Replies(props) {
  let content;
  if (props.replies.length === 0) {
    content = (
      <div className="activity_feed_primer">
        <span>Nothing to see here yet</span>
      </div>
    );
  } else {
    content = (
      <div className="activity_feed_collection">
        {props.activities.map((activity) => {
          return (
            <ActivityItem
              setReplyActivity={props.setReplyActivity}
              setPopped={props.setPopped}
              key={activity.uuid}
              activity={activity}
            />
          );
        })}
      </div>
    );
  }

  return <div>{content}</div>;
}