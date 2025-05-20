// index.ts
import { Client } from "pg";
import bcrypt from "bcrypt";
import "dotenv/config";
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './src/routes/auth.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// PostgreSQL client
const client = new Client({
  user: process.env.PG_USER || "postgres",
  host: process.env.PG_HOST || "localhost",
  database: process.env.PG_DATABASE || "kafka_resume",
  password: process.env.PG_PASSWORD,
  port: Number(process.env.PG_PORT) || 5432,
});

async function ensureConnected() {
  try {
    await client.connect();
  } catch (err: any) {
    // If already connected, ignore the error
    if (err.code !== '57P01' && !err.message.includes('Client has already been connected')) {
      throw err;
    }
  }
}

// Sign-up: Store user with hashed password
async function signup(email: string, password: string, name?: string) {
  await ensureConnected();
  const hashedPassword = await bcrypt.hash(password, 10);
  const query = `
    INSERT INTO users (email, password, name)
    VALUES ($1, $2, $3)
    RETURNING id, email, name, created_at;
  `;
  try {
    const result = await client.query(query, [email, hashedPassword, name]);
    return {
      success: true,
      user: result.rows[0],
    };
  } catch (err: any) {
    return {
      success: false,
      message: err.detail?.includes("already exists")
        ? "Email already exists"
        : "Failed to create account",
    };
  }
}

// Login: Verify credentials
async function login(email: string, password: string) {
  await ensureConnected();
  const query = `
    SELECT * FROM users
    WHERE email = $1;
  `;
  try {
    const result = await client.query(query, [email]);
    const user = result.rows[0];
    if (!user) {
      return { success: false, message: "User not found" };
    }
    const match = await bcrypt.compare(password, user.password);
    if (!match) {
      return { success: false, message: "Invalid password" };
    }
    return {
      success: true,
      user: { id: user.id, email: user.email, name: user.name },
    };
  } catch (err) {
    return { success: false, message: "Login failed" };
  }
}

// Routes
app.use('/api/auth', authRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: 'Something went wrong!'
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});