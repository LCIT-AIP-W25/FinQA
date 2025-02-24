import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
// import Dashboard from './components/Dashboard';
import Login from './components/Login';
import Signup from './components/Signup';
import Forget from './components/forget';
import ChatPage from './components/ChatPage';
import '../src/styles/custom.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import Comp from './components/Comp'

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path='/signup' element={<Signup />} />
          <Route path='/login' element={<Login />} />
          {/* <Route path='/dashboard' element={<ProtectedRoute><Dashboard /></ProtectedRoute>} /> */}
          <Route path='/chat' element={<ProtectedRoute><ChatPage /></ProtectedRoute>} />
          <Route path='/forget' element={<Forget />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}


export default App;