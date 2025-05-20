import { Pool } from 'pg';
import dotenv from 'dotenv';

dotenv.config();

// Validate required environment variables
const requiredEnvVars = ['PG_USER', 'PG_PASSWORD', 'PG_DATABASE'];
const missingEnvVars = requiredEnvVars.filter(envVar => !process.env[envVar]);

if (missingEnvVars.length > 0) {
  console.error('Missing required environment variables:', missingEnvVars.join(', '));
  process.exit(1);
}

const pool = new Pool({
  user: process.env.PG_USER,
  host: process.env.PG_HOST || 'localhost',
  database: process.env.PG_DATABASE,
  password: process.env.PG_PASSWORD,
  port: Number(process.env.PG_PORT) || 5432,
});

// Test the connection
pool.connect()
  .then(() => {
    console.log('Successfully connected to PostgreSQL database!');
    console.log('Database configuration:', {
      host: process.env.PG_HOST,
      port: process.env.PG_PORT,
      database: process.env.PG_DATABASE,
      user: process.env.PG_USER
    });
  })
  .catch(err => {
    console.error('Error connecting to the database:', err);
    process.exit(1);
  });

export default pool; 