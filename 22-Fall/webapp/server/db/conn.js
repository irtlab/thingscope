const { MongoClient } = require('mongodb');
const connectionString = process.env.ATLAS_URI || 'mongodb://localhost:27017';
const dbName = process.env.IOT_DB_NAME || 'iot';
const client = new MongoClient(connectionString, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

let dbConnection;

module.exports = {
  connectToServer: function (callback) {
    client.connect(function (err, db) {
      if (err || !db) {
        return callback(err);
      }

      dbConnection = db.db(dbName);
      console.log('Successfully connected to MongoDB.');

      return callback();
    });
  },

  getDb: function () {
    return dbConnection;
  },
};
