import { promises as fs } from 'fs';
import mongodb from 'mongodb';


export async function getAmazonDocumentDB() {
  // Specify the Amazon DocumentDB cert
  const ca = [await fs.readFile('rds-combined-ca-bundle.pem')];

  const url = 'mongodb://thingscope:thingscope123*@thingscope-2020-10-06-00-17-45.cluster-cy9ej67us89r.us-east-2.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false';
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
