import "./ConfirmationPage.css";
import React from "react";
import { useParams } from "react-router-dom";
import { ReactComponent as Logo } from "../components/svg/logo.svg";

// [TODO] Authenication
import { Auth, Hub } from "aws-amplify";

export default function ConfirmationPage() {
  const [code, setCode] = React.useState("");
  const [errors, setErrors] = React.useState("");
  const [codeSent, setCodeSent] = React.useState(false);

  const url = window.location.href;

  // Create a URLSearchParams object from the URL
  const searchParams = new URLSearchParams(new URL(url).search);

  // Get the value of the 'email' parameter from the URL
  const _email = searchParams.get("email");
  console.log(_email);

  const [email, setEmail] = React.useState(_email);

  // This way the user Email is put As they proceed to put in their confirmation code
  const code_onchange = (event) => {
    setCode(event.target.value);
  };
  const email_onchange = (event) => {
    setEmail(event.target.value);
  };

  const resend_code = async (event) => {
    setErrors("");
    try {
      await Auth.resendSignUp(email);
      console.log("code resent successfully");
      setCodeSent(true);
    } catch (err) {
      // does not return a code
      // does cognito always return english
      // for this to be an okay match?
      console.log(err);
      if (err.message === "Username cannot be empty") {
        setErrors(
          "You need to provide an email in order to send Resend Activiation Code"
        );
      } else if (err.message === "Username/client id combination not found.") {
        setErrors("Email is invalid or cannot be found.");
      }
    }
  };

  const handleAutoSignIn = ({ payload }) => {
    const { event } = payload;
    if (event === "autoSignIn") {
      const user = payload.data;
      console.log(user);
      localStorage.setItem(
        "access_token",
        user.signInUserSession.accessToken.jwtToken
      );
      window.location.href = "/";
    }
  };

  Hub.listen("auth", handleAutoSignIn);

  const onsubmit = async (event) => {
    event.preventDefault();
    setErrors("");
    try {
      await Auth.confirmSignUp(email, code);
      window.location.href = "/";
    } catch (error) {
      setErrors(error.message);
    }
    return false;
  };

  let el_errors;
  if (errors) {
    el_errors = <div className="errors">{errors}</div>;
  }

  let code_button;
  if (codeSent) {
    code_button = (
      <div className="sent-message">
        A new activation code has been sent to your email
      </div>
    );
  } else {
    code_button = (
      <button className="resend" onClick={resend_code}>
        Resend Activation Code
      </button>
    );
  }

  return (
    <article className="confirm-article">
      <div className="recover-info">
        <Logo className="logo" />
      </div>
      <div className="recover-wrapper">
        <form className="confirm_form" onSubmit={onsubmit}>
          <h2>Confirm your Email</h2>
          <div className="fields">
            <div className="field text_field email">
              <label>Email</label>
              <input type="text" value={email} onChange={email_onchange} />
            </div>
            <div className="field text_field code">
              <label>Confirmation Code</label>
              <input type="text" value={code} onChange={code_onchange} />
            </div>
          </div>
          {el_errors}
          <div className="submit">
            <button type="submit">Confirm Email</button>
          </div>
        </form>
      </div>
      {code_button}
    </article>
  );
}
