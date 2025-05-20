import { Pool } from 'pg';

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'kafka_resume',
  password: '2006', // Replace with your actual password
  port: 5432,
});

export default pool; 