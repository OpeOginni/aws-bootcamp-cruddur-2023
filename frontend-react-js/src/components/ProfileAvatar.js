import "./ProfileAvatar.css";
import React, { useState, useEffect } from "react";

export default function ProfileAvatar(props) {

    const backgroundImage = `url("https://assets.opeoginni.cloud/avatars/${props.id}.jpg")`

    const styles = {
        backgroundImage: backgroundImage,
        backgroundSize: 'cover',
        backgroundPosition: 'center'
    }

  return (
    <div 
        className="profile-avatar"
        style={styles}
        ></div>
    );
}