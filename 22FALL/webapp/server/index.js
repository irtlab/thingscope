const express = require("express"); 
const req = require("express/lib/request");
const { ObjectId } = require('mongodb');

// get MongoDB driver connection
const dbo = require('./db/conn');


const PORT = process.env.PORT || 3001;


const app = express();

app.use(express.json());
app.use(express.urlencoded());

app.post('/device/:id', (req, res) => {
  // Reading id from the URL
 
  const id = req.params.id;
  const newRow = req.body;
  console.log("req", req.body)

  //filter = { '_id' : ObjectId(req.params._id) }
  filter = { 'mac_addr' : req.body.row.mac_addr}
  modifications ={ '$set' : { 'mfgr' : req.body.row.mfgr, 'device' : req.body.row.device, 'name' : req.body.row.name, 'device_type': req.body.row.device_type } }
  
  const dbConnect = dbo.getDb();

  result = dbConnect.collection('devices').updateOne(filter, modifications)

  console.log('Update Result', result)
  
  result = dbConnect.collection('devices').findOne(filter)

  res.json(result);
});

app.get("/endpoints-del/:mac", (req, res) => {

  if(req.params.mac === '1') {
    res.json([{
      _id: {
        $oid: "6396c45965ea33d51505f9ac",
      },
      port: "80/tcp",
      ip: "89.30.121.150",
      security_posture: "UNKNOWN",
      domain_name: "scalews.withings.net",
      location: {
        city: "Paris",
        region: "Île-de-France",
        country: "France",
      },
      device_mac: "00:24:e4:24:80:2a",
    },])

    return
  }
  
  res.json([
    {
      _id: {
        $oid: "6396c45965ea33d51505f9ac",
      },
      port: "80/tcp",
      ip: "89.30.121.150",
      security_posture: "UNKNOWN",
      domain_name: "scalews.withings.net",
      location: {
        city: "Paris",
        region: "Île-de-France",
        country: "France",
      },
      device_mac: "00:24:e4:24:80:2a",
    },
    {
      _id: {
        $oid: "6396c45b52082a9ccdb907e7",
      },
      port: "80/tcp",
      ip: "89.30.121.150",
      security_posture: "UNKNOWN",
      domain_name: "scalews.withings.net",
      location: {
        city: "Paris",
        region: "Île-de-France",
        country: "France",
      },
      device_mac: "00:24:e4:24:80:2a",
    },
    {
      _id: {
        $oid: "6396c45d9a8ac83d46e6fbe3",
      },
      port: "80/tcp",
      ip: "89.30.121.150",
      security_posture: "UNKNOWN",
      domain_name: "scalews.withings.net",
      location: {
        city: "Paris",
        region: "Île-de-France",
        country: "France",
      },
      device_mac: "00:24:e4:24:80:2a",
    },
    {
      _id: {
        $oid: "6396c45fc926d90f97a5a334",
      },
      port: "80/tcp",
      ip: "89.30.121.150",
      security_posture: "UNKNOWN",
      domain_name: "scalews.withings.net",
      location: {
        city: "Paris",
        region: "Île-de-France",
        country: "France",
      },
      device_mac: "00:24:e4:24:80:2a",
    },
    {
      _id: "89.30.121.150",
      port: "80/tcp",
      ip: "89.30.121.150",
      security_posture: "UNKNOWN",
      domain_name: "scalews.withings.net",
      location: {
        city: "Paris",
        region: "Île-de-France",
        country: "France",
      },
      device_mac: "00:24:e4:24:80:2a",
    },
  ]);
});

app.get('/endpoints/:mac',  (_req, res) => {
  const dbConnect = dbo.getDb();

  dbConnect
    .collection('endpoints')
    .find({'device_mac' : _req.params.mac})
    .limit(500)
    .toArray(function (err, result) {
      if (err) {
        res.status(400).send('Error fetching listings!');
      } else {

        var processed = result.map( (r) => {
          r["city"] = r.location ? r.location.city :''
          r["region"] = r.location ? r.location.region :''
          r["country"] = r.location ? r.location.country :''
          r["ip_org"] = r.location ? r.location.org :''
          r["ip_version"] = r.location ? r.location.version :''
          r["coordinates"] = r.location ? r.location.latitude + ',' + r.location.longitude :''
          return r
          }
        );
        
        res.json(result);
      }
    });
});

app.get('/endpoints',  (_req, res) => {
  const dbConnect = dbo.getDb();

  dbConnect
    .collection('endpoints')
    .find({})
    .limit(500)
    .toArray(function (err, result) {
      if (err) {
        res.status(400).send('Error fetching listings!');
      } else {

        var processed = result.map( (r) => {
          r["city"] = r.location ? r.location.city :''
          r["region"] = r.location ? r.location.region :''
          r["country"] = r.location ? r.location.country :''
          r["ip_org"] = r.location ? r.location.org :''
          r["ip_version"] = r.location ? r.location.version :''
          r["coordinates"] = r.location ? r.location.latitude + ',' + r.location.longitude :''
          return r
          }
        );
        
        res.json(result);
      }
    });
});


app.get('/devices',  (_req, res) => {
  const dbConnect = dbo.getDb();

  dbConnect
    .collection('devices')
    .find({'enabled' : true})
    .limit(500)
    .toArray(function (err, result) {
      if (err) {
        res.status(400).send('Error fetching listings!');
      } else {
        res.json(result);
      }
    });
});

app.get('/domainips',  (_req, res) => {
  const dbConnect = dbo.getDb();

  dbConnect
    .collection('domainips')
    .find({})
    .limit(1000)
    .toArray(function (err, result) {
      if (err) {
        res.status(400).send('Error fetching listings!');
      } else {
        res.json(result);
      }
    });
});


// perform a database connection when the server starts
dbo.connectToServer(function (err) {
  if (err) {
    console.error(err);
    process.exit();
  }

  app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
  });

});
