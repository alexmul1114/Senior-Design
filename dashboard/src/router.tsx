import { createBrowserRouter, createRoutesFromElements, Route } from 'react-router-dom';
import App from './App';
import HomePage from './pages/HomePage';
import DocumentPage from './pages/DocumentPage';
import StatsPage from './pages/StatsPage';
import MarketPage from './pages/MarketPage';
import AdvertisingPage from './pages/AdvertisingPage';
import ContactPage from './pages/ContactPage';

/**
 * The router is defined with a root route that renders the <App /> layout.
 * Nested routes will render in <Outlet /> inside App.
 */
const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<App />}>
      <Route index element={<HomePage />} />
      <Route path="documents" element={<DocumentPage />} />
      <Route path="stats" element={<StatsPage />} />
      <Route path="market" element={<MarketPage />} />
      <Route path="advertising" element={<AdvertisingPage />} />
      <Route path="contact" element={<ContactPage />} />
    </Route>
  )
);

export default router;
