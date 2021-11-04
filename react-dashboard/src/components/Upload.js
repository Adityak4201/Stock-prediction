import React, { useState, useEffect, forwardRef } from "react";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert from "@mui/material/Alert";
import axios from "axios";

const Alert = forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState([]);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const [open, setOpen] = React.useState(false);

  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }

    setOpen(false);
  };

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
        console.log(res.data);
        // console.log(res.data);
        setSuccess("File uploaded successfully!!");
      })
      .catch((err) => {
        console.log(err.response);
        if (err.response.status === 403) setError(err.response.data.error);
        else if (err.response.status === 406) setError(err.response.data.error);
        else setError("Server isn't responding!! Please try again later");
      });
    setOpen(true);
  };

  useEffect(() => {
    console.log(selectedFile[0]);
  }, [selectedFile]);

  const vertical = "top",
    horizontal = "center";

  return (
    <div>
      <label htmlFor="upload">Upload Files:</label>&nbsp;
      <input
        name="Upload"
        type="file"
        onChange={(e) => setSelectedFile(e.target.files)}
        multiple
      />
      <input type="button" value="Upload Files" onClick={handleUpload} />
      {error && (
        <Snackbar
          open={open}
          autoHideDuration={6000}
          onClose={handleClose}
          anchorOrigin={{ vertical, horizontal }}
        >
          <Alert onClose={handleClose} severity="error">
            {error}
          </Alert>
        </Snackbar>
      )}
      {success && (
        <Snackbar
          open={open}
          autoHideDuration={6000}
          onClose={handleClose}
          anchorOrigin={{ vertical, horizontal }}
        >
          <Alert onClose={handleClose} severity="success">
            {success}
          </Alert>
        </Snackbar>
      )}
    </div>
  );
};

export default Upload;
