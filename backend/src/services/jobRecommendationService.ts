// backend/src/services/jobRecommendationService.ts
import pool from '../config/database.js';

interface JobFilters {
  location?: string;
  keywords?: string;
  days_posted?: number;
  min_match_score?: number;
}

export class JobRecommendationService {
  /**
   * Get jobs from database with filters
   */
  async getJobs(filters?: JobFilters): Promise<any[]> {
    try {
      let query = 'SELECT * FROM jobs WHERE is_active = true';
      const params: any[] = [];
      let paramIndex = 1;

      // Filter by location
      if (filters?.location) {
        query += ` AND (LOWER(location) LIKE $${paramIndex} OR LOWER(location) = 'remote')`;
        params.push(`%${filters.location.toLowerCase()}%`);
        paramIndex++;
      }

      // Filter by keywords in title or description
      if (filters?.keywords) {
        query += ` AND (
          LOWER(title) LIKE $${paramIndex} OR 
          LOWER(description) LIKE $${paramIndex}
        )`;
        params.push(`%${filters.keywords.toLowerCase()}%`);
        paramIndex++;
      }

      // Filter by days posted
      if (filters?.days_posted) {
        query += ` AND posted_date >= NOW() - INTERVAL '${filters.days_posted} days'`;
      }

      query += ' ORDER BY posted_date DESC LIMIT 100';

      const result = await pool.query(query, params);
      return result.rows;
    } catch (error) {
      console.error('Error fetching jobs from database:', error);
      return [];
    }
  }

  /**
   * Store job recommendations in database
   */
  async storeRecommendations(
    userId: number,
    resumeId: number,
    recommendations: any[]
  ): Promise<void> {
    const client = await pool.connect();
    try {
      await client.query('BEGIN');

      // Clear old recommendations for this user and resume
      await client.query(
        'DELETE FROM job_recommendations WHERE user_id = $1 AND resume_id = $2',
        [userId, resumeId]
      );

      // Insert new recommendations
      for (const rec of recommendations) {
        // First, ensure the job exists in the jobs table
        const jobCheck = await client.query(
          'SELECT id FROM jobs WHERE url = $1',
          [rec.link]
        );

        let jobId: number;

        if (jobCheck.rows.length === 0) {
          // Insert the job if it doesn't exist
          const jobInsert = await client.query(
            `INSERT INTO jobs (
              title, company, location, description, url, posted_date,
              salary, tags, source, experience_required, job_type, is_active
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            RETURNING id`,
            [
              rec.title,
              rec.company || 'Unknown',
              rec.location,
              rec.snippet,
              rec.link,
              rec.updated || new Date().toISOString(),
              rec.salary || 'Not specified',
              [],
              rec.source || 'jooble',
              'Not specified',
              rec.type || 'Full-time',
              true
            ]
          );
          jobId = jobInsert.rows[0].id;
        } else {
          jobId = jobCheck.rows[0].id;
        }

        // Insert recommendation
        await client.query(
          `INSERT INTO job_recommendations 
           (user_id, resume_id, job_id, match_score, recommendation_reasons)
           VALUES ($1, $2, $3, $4, $5)
           ON CONFLICT (user_id, resume_id, job_id) DO UPDATE
           SET match_score = $4, recommendation_reasons = $5`,
          [
            userId,
            resumeId,
            jobId,
            rec.matchScore,
            JSON.stringify(rec.recommendationReasons || [])
          ]
        );
      }

      await client.query('COMMIT');
      console.log(`Stored ${recommendations.length} recommendations for user ${userId}`);
    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Error storing recommendations:', error);
      throw error;
    } finally {
      client.release();
    }
  }

  /**
   * Get stored recommendations for a user
   */
  async getUserRecommendations(userId: number, limit: number = 20): Promise<any[]> {
    try {
      const result = await pool.query(
        `SELECT 
          r.id as recommendation_id,
          r.match_score,
          r.recommendation_reasons,
          r.created_at,
          j.id as job_id,
          j.title, 
          j.company, 
          j.location, 
          j.description, 
          j.url, 
          j.posted_date, 
          j.salary, 
          j.tags, 
          j.experience_required, 
          j.job_type,
          j.source
         FROM job_recommendations r
         JOIN jobs j ON r.job_id = j.id
         WHERE r.user_id = $1 AND j.is_active = true
         ORDER BY r.match_score DESC, r.created_at DESC
         LIMIT $2`,
        [userId, limit]
      );

      return result.rows;
    } catch (error) {
      console.error('Error fetching user recommendations:', error);
      return [];
    }
  }
}

export default new JobRecommendationService();