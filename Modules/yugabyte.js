const { Client } = require('pg');

async function connectToYugabyteDB() {
    const client = new Client({
        user: 'keerthi-NMS',
        host: 'Global-keerthi-NMS-1c1b4b7e-1',
        database: 'NMS',
        password: 'bcsudueib02',
        port: 'auto',
    });

    try {
        await client.connect();
        console.log('Connected to YugabyteDB');

        await createTable(client);
        await insertData(client);
        await retrieveData(client);
    } catch (error) {
        console.error('Error connecting to YugabyteDB:', error);
    } finally {
        await client.end();
        console.log('Disconnected from YugabyteDB');
    }
}

async function createTable(client) {
    const createTableQuery = `
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        )
    `;

    try {
        await client.query(createTableQuery);
        console.log('Table created successfully');
    } catch (error) {
        console.error('Error creating table:', error);
    }
}

async function insertData(client) {
    const insertDataQuery = `
        INSERT INTO users (name, email)
        VALUES ('John Doe', 'john.doe@example.com')
    `;

    try {
        await client.query(insertDataQuery);
        console.log('Data inserted successfully');
    } catch (error) {
        console.error('Error inserting data:', error);
    }
}

async function retrieveData(client) {
    const retrieveDataQuery = 'SELECT * FROM users';

    try {
        const result = await client.query(retrieveDataQuery);
        console.log('Data retrieved successfully:', result.rows);
    } catch (error) {
        console.error('Error retrieving data:', error);
    }
}

connectToYugabyteDB();