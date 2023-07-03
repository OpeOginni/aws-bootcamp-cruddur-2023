import "./ActivityShowPage.css";
import React from "react";
import { useParams } from "react-router-dom";

import DesktopNavigation from "components/DesktopNavigation";
import DesktopSidebar from "components/DesktopSidebar";
import ActivityForm from "components/ActivityForm";
import ReplyForm from "components/ReplyForm";
import Replies from "components/Replies";
import ActivityItem from "components/ActivityItem";

import { checkAuth } from "lib/CheckAuth";
import { get } from "lib/Requests";

export default function ActivityShowPage() {
  const [activity, setActivity] = React.useState(null);
  const [replies, setReplies] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const params = useParams();

  const loadData = async () => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/@${params.handle}/status/${params.activity_uuid}`;
    get(url, {
      auth: false,

      success: function (data) {
        setActivity(data.activity);
        setReplies(data.replies);
      },
    });
  };

  // check if we are authenicated

  // check when the page loads if we are authenicated

  React.useEffect(() => {
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth(setUser);
  }, []);

  let el_activity;
  if (activity !== null) {
    el_activity = (
      <ActivityItem
        setReplyActivity={setReplyActivity}
        setPopped={setPoppedReply}
        activity={activity}
      />
    );
  }
  return (
    <article>
      <DesktopNavigation user={user} active={"home"} setPopped={setPopped} />
      <div className="content">
        <ActivityForm
          user_handle={user}
          popped={popped}
          setPopped={setPopped}
        />
        <ReplyForm
          activity={replyActivity}
          popped={poppedReply}
          setPopped={setPoppedReply}
        />
        <div className="activity_feed">
          <div className="activity_feed_heading">
            <div className="title">Home</div>
          </div>
          {el_activity}
          <Replies
            title="Home"
            setReplyActivity={setReplyActivity}
            setPopped={setPoppedReply}
            replies={replies}
          />
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}
