import { promises as fs } from 'fs';
import mongodb from 'mongodb';
import 'dotenv/config';

export async function getAmazonDocumentDB() {
  // Specify the Amazon DocumentDB cert
  const ca = [await fs.readFile('rds-combined-ca-bundle.pem')];

  const url = process.env.MONGODB_URL;
  const options = {
    poolSize: 64,
    useUnifiedTopology: true,
    sslValidate: true,
    sslCA: ca,
    useNewUrlParser: true
  };

  try {
    const client = await mongodb.MongoClient.connect(url, options);
    const mongo_db = client.db('thingscope_db');
    if (!mongo_db) {
      client.close();
      throw new Error('Amazon DocumentDB connection failed');
    }
    return mongo_db;
  } catch (error) {
    throw new Error(error);
  }
}
