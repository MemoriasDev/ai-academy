/**
 * Environment variable validation and security checks
 * Ensures proper configuration and prevents service role key exposure
 */

const REQUIRED_ENV_VARS = [
  'VITE_SUPABASE_URL',
  'VITE_SUPABASE_ANON_KEY'
] as const;

const FORBIDDEN_ENV_VARS = [
  'VITE_SUPABASE_SERVICE_ROLE_KEY',
  'VITE_SERVICE_ROLE_KEY',
  'VITE_SERVICE_KEY'
] as const;

export function validateEnv(): void {
  // Check for required variables
  const missing = REQUIRED_ENV_VARS.filter(key => !import.meta.env[key]);
  
  if (missing.length > 0) {
    console.error(`❌ Missing required environment variables: ${missing.join(', ')}`);
    console.error('Please check your .env.local file');
    throw new Error('Missing required environment variables');
  }

  // Check for forbidden variables (service role keys)
  const exposed = FORBIDDEN_ENV_VARS.filter(key => import.meta.env[key]);
  
  if (exposed.length > 0) {
    console.error('🚨 SECURITY ERROR: Service role key detected in frontend environment!');
    console.error(`Found: ${exposed.join(', ')}`);
    console.error('Service role keys must NEVER be exposed to the frontend.');
    console.error('Remove these from your .env files or remove the VITE_ prefix.');
    throw new Error('Service role key exposure detected');
  }

  // Validate URL format
  const url = import.meta.env.VITE_SUPABASE_URL;
  if (!url.startsWith('https://') && !url.startsWith('http://localhost')) {
    console.warn('⚠️ Supabase URL should use HTTPS in production');
  }

  // Validate anon key format (basic JWT structure check)
  const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;
  if (!anonKey.includes('.')) {
    console.error('❌ Invalid Supabase anon key format');
    throw new Error('Invalid Supabase anon key');
  }

  // Environment variables validated successfully
}

// Run validation immediately when module is imported
if (import.meta.env.MODE !== 'test') {
  validateEnv();
}