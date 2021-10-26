import React, { useState, useEffect } from "react";
import axios from "axios";

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState([]);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const handleUpload = () => {
    const formData = new FormData();
    formData.append("file-0", selectedFile[0]);
    formData.append("file-1", selectedFile[1]);
    console.log(formData);
    setError("");
    setSuccess("");
    axios
      .post(
        "https://5000-beige-toucan-vl0mh6dp.ws-us17.gitpod.io/upload",
        formData
      )
      .then((res) => {
        console.log(res.data.real);
        console.log(res.data.predicted);
        setSuccess("File uploaded successfully!!");
      })
      .catch((err) => {
        console.log(err.response);
        if (err.response.status === 403) setError(err.response.data.error);
        else if (err.response.status === 406) setError(err.response.data.error);
        else setError("Server isn't responding!! Please try again later");
      });
  };

  useEffect(() => {
    console.log(selectedFile[0]);
  }, [selectedFile]);

  return (
    <div>
      <p>{error ? error : success}</p>
      <label htmlFor="upload">Upload Files:</label>&nbsp;
      <input
        name="Upload"
        type="file"
        onChange={(e) => setSelectedFile(e.target.files)}
        multiple
      />
      <input type="button" value="Upload Files" onClick={handleUpload} />
    </div>
  );
};

export default Upload;
