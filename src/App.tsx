/**
 * @description 
 * Main application component for Module Mind.
 * Sets up providers, routing, and authentication protection.
 * 
 * Component hierarchy (order matters):
 * 1. QueryClientProvider - React Query for data fetching
 * 2. TooltipProvider - Global tooltip context
 * 3. Toasters - Notification systems
 * 4. BrowserRouter - Must wrap AuthProvider for useNavigate
 * 5. AuthProvider - Must be inside BrowserRouter
 * 6. Routes with ProtectedRoute wrapper
 * 
 * @notes
 * - AuthProvider MUST be inside BrowserRouter to use useNavigate hook
 * - All course content routes are protected with ProtectedRoute
 * - Login page removed (authentication handled via modal)
 * - NotFound page remains public for 404 errors
 */

import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            {/* Protected route - all course content */}
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <Index />
                </ProtectedRoute>
              } 
            />
            
            {/* Public routes (currently just 404) */}
            {/* Future: Add public pages like /about, /pricing here */}
            
            {/* Catch-all for 404 */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;