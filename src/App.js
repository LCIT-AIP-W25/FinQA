import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './components/Login';
import Signup from './components/Signup';
import Forget from './components/forget';
import ChatPage from './components/ChatPage';
import PDFChatPage from "./components/PDFChatPage";
import HomePage from './components/HomePage';
import TradingAssistant from './components/TradingAssistant'; // ✅ NEW
import '../src/styles/custom.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import ResetPassword from './components/ResetPassword';
import VerifyEmail from "./components/VerifyEmail";
import { LoaderProvider } from './components/LoaderContext';
import GlobalLoader from './components/GlobalLoader';

function App() {
  return (
    <LoaderProvider>
      <GlobalLoader />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path='/signup' element={<Signup />} />
          <Route path='/login' element={<Login />} />
          <Route path='/home' element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
          <Route path='/chat' element={<ProtectedRoute><ChatPage /></ProtectedRoute>} />
          <Route path='/forget' element={<Forget />} />
          <Route path="/reset_password/:token" element={<ResetPassword />} />
          <Route path="/verify_email/:token" element={<VerifyEmail />} />
          <Route path='/pdf-chat' element={<ProtectedRoute><PDFChatPage /></ProtectedRoute>} />
          <Route path='/trading-assistant' element={<ProtectedRoute><TradingAssistant /></ProtectedRoute>} /> {/* ✅ FIXED */}
        </Routes>
      </BrowserRouter>
    </LoaderProvider>
  );
}

export default App;
