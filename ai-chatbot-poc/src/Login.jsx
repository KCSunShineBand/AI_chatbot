import React, { useState } from 'react';
import { TextField, Button, Snackbar, Container, Box } from '@mui/material';
import MuiAlert from '@mui/material/Alert';
// import { useNavigate } from 'react-router-dom';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [severity, setSeverity] = useState('success');

  // const navigate = useNavigate();

  const handleSubmit = () => {


    if (username === process.env.REACT_APP_USERNAME && password === process.env.REACT_APP_PASSWORD) {
      setSeverity('success');
      setMessage('Login successful!');
      setOpen(true);
      console.log("login worked");
      setTimeout(() => {
        window.location.href = 'https://aikcwongdeploy-xm28yozttp9bsjjuxky5uc.streamlit.app/';
      }, 1500);
      } else {
        setSeverity('error');
        setMessage('Login has failed!');
        setOpen(true);
        console.log("login failed");
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
        >
          Sign In
        </Button>
        <Snackbar open={open} autoHideDuration={1500} onClose={() => setOpen(false)}>
          <Alert onClose={() => setOpen(false)} severity={severity} sx={{ width: '100%' }}>
            {message}
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
}

export default Login;
