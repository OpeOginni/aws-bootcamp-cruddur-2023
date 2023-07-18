import "./UserFeedPage.css";
import React from "react";
import { useParams } from "react-router-dom";

import DesktopNavigation from "components/DesktopNavigation";
import DesktopSidebar from "components/DesktopSidebar";
import ActivityFeed from "components/ActivityFeed";
import ActivityForm from "components/ActivityForm";
import ProfileHeading from "components/ProfileHeading";
import ProfileForm from "components/ProfileForm";

import { checkAuth } from "lib/CheckAuth";
import { get } from "lib/Requests";

export default function UserFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [poppedProfile, setPoppedProfile] = React.useState([]);

  const [profile, setProfile] = React.useState([]);

  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const params = useParams();

  const loadData = async () => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/@${params.handle}`;
    get(url, {
      auth: false,
      success: function (data) {
        setProfile(data.profile);
        setActivities(data.activities);
      },
    });
  };

  React.useEffect(() => {
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth(setUser);
  }, []);

  let profileHeading;

  let desktopNavigation;

  // This makes the Profile heading to only render when the User and Profile Detail has been fetched
  if (profile && user) {
    profileHeading = (
      <ProfileHeading
        setPopped={setPoppedProfile}
        user={user}
        profile={profile}
      />
    );

    if (profile.cognito_user_uuid == user.cognito_user_uuid) {
      desktopNavigation = (
        <DesktopNavigation
          user={user}
          active={"profile"}
          setPopped={setPopped}
        />
      );
    } else {
      desktopNavigation = (
        <DesktopNavigation user={user} setPopped={setPopped} />
      );
    }
  }

  if (profile && user) {
    profileHeading = (
      <ProfileHeading
        setPopped={setPoppedProfile}
        user={user}
        profile={profile}
      />
    );
  }

  return (
    <article>
      {/* 
      Only when you view your profile will the Profile Link Glow
      It wont glow when you are viewing the profile of others
       */}
      {desktopNavigation}
      <div className="content">
        <ActivityForm popped={popped} setActivities={setActivities} />

        <ProfileForm
          profile={profile}
          popped={poppedProfile}
          setPopped={setPoppedProfile}
        />

        <div className="activity_feed">
          {profileHeading}
          <ActivityFeed title={params.handle} activities={activities} />
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}
