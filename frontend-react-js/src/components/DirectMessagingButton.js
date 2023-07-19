import "./DirectMessagingButton.css";
import { ReactComponent as MessagesIcon } from "./svg/messages.svg";
import { get } from "lib/Requests";

export default function DirectMessagingButton(props) {
  function directMessage() {
    // This function will check if a user and another user already have a current chat
    // If yes the user is redirected to that chat group
    // If not they are redirect to create a new chat group
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/messages/exist/${props.receiver.handle}`;
    get(url, {
      auth: true,
      success: function (data) {
        redirect(data);
      },
    });
  }

  function redirect(data) {
    if (data.exists) {
      // Redirects to Existing Message Group
      window.location.href = `/messages/${data.message_group_uuid}`;
    } else {
      // Redirects to New Message Group
      window.location.href = `/messages/new/${props.receiver.handle}`;
    }
  }

  return (
    <div onClick={directMessage} className="button_container">
      <MessagesIcon className="icon "></MessagesIcon>
    </div>
  );
}
