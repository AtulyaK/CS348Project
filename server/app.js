const express = require('express');
const path = require('path');
const { Client } = require('pg');  // PostgreSQL client

const app = express();
const port = 3000;

// PostgreSQL connection setup
//const client = new Client({
//  host: 'localhost',
//   user: 'your_db_user',
// database: 'your_db_name',
// password: 'your_db_password',
// port: 5432
// });

//client.connect();

// Serve static files (HTML, CSS, JS) from /public folder
app.use(express.static(path.join(__dirname, '../public')));

// Example route for the backend to fetch data from the database
app.get('/api/data', async (req, res) => {
  try {
    const result = await client.query('SELECT * FROM your_table');
    res.json(result.rows);  // Send the result as JSON
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
