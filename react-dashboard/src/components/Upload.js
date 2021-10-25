import React, { useState } from "react";
import axios from "axios";

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState("");

  const handleUpload = () => {
    const formData = new FormData();
    formData.append("file", selectedFile);

    axios
      .post(
        "https://5000-beige-toucan-vl0mh6dp.ws-us17.gitpod.io/upload",
        formData
      )
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err.response);
      });
  };

  return (
    <div>
      <label htmlFor="upload">Upload Files:</label>&nbsp;
      <input
        name="Upload"
        type="file"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />
      <input type="button" value="Upload Files" onClick={handleUpload} />
    </div>
  );
};

export default Upload;
