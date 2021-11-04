import React, { useState, forwardRef } from "react";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert from "@mui/material/Alert";
import axios from "axios";
import "./Upload.css";
import Graph from "./Graph";

const Alert = forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState([]);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

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
    setLoading(true);
    axios
      .post(
        "https://5000-beige-toucan-vl0mh6dp.ws-us17.gitpod.io/upload",
        formData
      )
      .then((res) => {
        setLoading(false);
        console.log(res.data);
        setData(res.data);
        // console.log(res.data);
        setSuccess("File uploaded successfully!!");
      })
      .catch((err) => {
        setLoading(false);
        console.log(err.response);
        if (err.response.status === 403) setError(err.response.data.error);
        else if (err.response.status === 406) setError(err.response.data.error);
        else if (err.response.status === 500)
          setError("Something went wrong!!!");
        else setError("Server isn't responding!! Please try again later");
      });
    setOpen(true);
  };

  // useEffect(() => {
  //   console.log(data);
  // }, [data]);

  const vertical = "top",
    horizontal = "center";

  return (
    <>
      <h1 className="heading">Stock Prediction</h1>
      <label htmlFor="upload" className="upload-label">
        Upload Files:
      </label>
      &nbsp;
      <input
        name="Upload"
        type="file"
        onChange={(e) => setSelectedFile(e.target.files)}
        multiple
      />
      <button type="button" className="upload-btn" onClick={handleUpload}>
        {loading ? (
          <>
            <span
              className="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            ></span>{" "}
            Loading...
          </>
        ) : (
          "Upload Files"
        )}
      </button>
      {loading ? (
        <h2 className="predict-text">
          Model is running and predicting the output
        </h2>
      ) : Object.keys(data).length ? (
        <Graph data={data} />
      ) : null}
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
    </>
  );
};

export default Upload;
