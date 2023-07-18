import "./ProfileHeading.css";
import EditProfileButton from "../components/EditProfileButton";
import ProfileAvatar from "./ProfileAvatar";
import DirectMessagingButton from "./DirectMessagingButton";

export default function ProfileHeading(props) {
  const backgroundImage =
    'url("https://assets.opeoginni.cloud/banners/banner.jpg")';

  // Users can uplaod Banners too
  // const backgroundImage = `url("https://assets.opeoginni.cloud/banners/${props.id}.jpg")`

  const styles = {
    backgroundImage: backgroundImage,
    backgroundSize: "cover",
    backgroundPosition: "center",
  };

  let editProfileButton;
  let directMessagingButton;

  //  This prevents Users from updating the profile of another User
  if (props.user.cognito_user_uuid == props.profile.cognito_user_uuid) {
    // If the user is the owner of the profile the edit profile button is rendered
    editProfileButton = <EditProfileButton setPopped={props.setPopped} />;
  } else {
    // Else if the user is NOT the owner of the profiile, a direct message button is rendered
    directMessagingButton = <DirectMessagingButton receiver={props.profile} />;
  }

  return (
    <div className="activity_feed_heading profile_heading">
      <div className="title">{props.profile.display_name}</div>
      <div className="cruds_count">{props.profile.cruds_count} Cruds</div>

      <div className="banner" style={styles}>
        <ProfileAvatar id={props.profile.cognito_user_uuid} />
      </div>

      <div className="info">
        <div className="id">
          <div className="display_name">{props.profile.display_name}</div>
          <div className="handle">@{props.profile.handle}</div>
        </div>
        {editProfileButton}
        {directMessagingButton}
      </div>
      <div className="bio">{props.profile.bio}</div>
    </div>
  );
}
