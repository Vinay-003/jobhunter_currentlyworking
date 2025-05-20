//extract the name of pdf file latest from the db (postgresql)
import { Client } from 'pg';

// Database configuration
const dbConfig = {
  user: 'your_username',
  host: 'localhost',
  database: 'your_database',
  password: 'your_password',
  port: 5432,
};

// Async function to fetch file name from PostgreSQL
async function getFileName(): Promise<string | null> {
  const client = new Client(dbConfig);

  try {
    // Connect to the database
    await client.connect();

    // Query to select a file name (modify condition as needed)
    const query = 'SELECT filename FROM files WHERE id = $1 LIMIT 1';
    const values = [1]; // Example: fetching file name for id = 1

    // Execute the query
    const result = await client.query(query, values);

    // Check if a row was returned
    if (result.rows.length > 0) {
      const fileName: string = result.rows[0].filename;
      return fileName;
    } else {
      console.log('No file name found');
      return null;
    }
  } catch (error) {
    console.error('Error fetching file name:', error);
    return null;
  } finally {
    // Close the database connection
    await client.end();
  }
}

// Example usage
async function main() {
  const fileName = await getFileName();
  if (fileName) {
    console.log('File name:', fileName);  //untoldCoding.pdf 


    

    
  } else {
    console.log('Failed to retrieve file name');
  }

// call the pdf from uploads and extract the text from it 
//using PDF.js
    const pdfPath = `uploads/${fileName}`;
    const pdfText = await extractTextFromPDF(pdfPath); //getTextContent(
    console.log('Extracted text:', pdfText);


}

main().catch(console.error);