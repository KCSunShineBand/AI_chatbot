import React, { useState } from 'react';
import { TextField, Button, Snackbar, Container, Box, CircularProgress, Typography } from '@mui/material';
import MuiAlert from '@mui/material/Alert';
import SmartToyIcon from '@mui/icons-material/SmartToy';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));


function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('error');

  const handleSubmit = async () => {
    try {
      if (username === process.env.REACT_APP_USERNAME && password === process.env.REACT_APP_PASSWORD) {
        console.log("login success");
        setSnackbarMessage('Login successful! Starting up AI engine...');
        setSnackbarSeverity('success');
        setOpenSnackbar(true);
        setLoading(true);

        // Wait for the state to update and Snackbar to render
        await delay(2000);

        window.location.href = 'https://aikcwongdeploy-xm28yozttp9bsjjuxky5uc.streamlit.app/';
      } else {
        console.log("login fail");
        setSnackbarMessage('Error logging in, please try again!');
        setSnackbarSeverity('error');
        setOpenSnackbar(true);

        // Wait for the state to update and Snackbar to render
        await delay(2000);

        // Any additional logic after showing the Snackbar can go here
      }
    } catch (error) {
      console.error("Error during login process:", error);
      // Handle any exceptions here
    }
  };



  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        {/* <Typography variant="h3" sx={{ textAlign: 'center' }}>
          Financial AI Chatbot <SmartToyIcon />
        </Typography> */}
        <img src="/woke_logo.png" alt="Woke Logo" style={{ maxWidth: '100%', height: 'auto' }} />

        <TextField
          margin="normal"
          required
          fullWidth
          label="Username"
          autoFocus
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <TextField
          margin="normal"
          required
          fullWidth
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Sign In'}
        </Button>
        {/* <Snackbar open={open} autoHideDuration={2000} onClose={handleClose}>
          <Alert onClose={handleClose} severity={severity} sx={{ width: '100%' }}>
            {message}
          </Alert>
        </Snackbar> */}
      </Box>
      <Snackbar
        open={openSnackbar}
        autoHideDuration={5000}
        onClose={() => setOpenSnackbar(false)}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={() => setOpenSnackbar(false)} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default Login;
