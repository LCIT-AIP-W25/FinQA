import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './components/Login';
import Signup from './components/Signup';
import Forget from './components/forget';
import ChatPage from './components/ChatPage';
import '../src/styles/custom.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import Comp from './components/Comp';

// ✅ Import Loader Context and Global Loader
import { LoaderProvider } from './components/LoaderContext';
import GlobalLoader from './components/GlobalLoader';

function App() {
  return (
    <LoaderProvider> {/* ✅ Wrap everything inside LoaderProvider */}
      <GlobalLoader />  {/* ✅ Add Global Loader */}
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path='/signup' element={<Signup />} />
          <Route path='/login' element={<Login />} />
          <Route path='/chat' element={<ProtectedRoute><ChatPage /></ProtectedRoute>} />
          <Route path='/forget' element={<Forget />} />
        </Routes>
      </BrowserRouter>
    </LoaderProvider>
  );
}

export default App;
