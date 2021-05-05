import express from 'express';
import mongodb from 'mongodb';
import { promises as fs } from 'fs';
import { BadRequestError, NotFoundError } from '../errors';
import { jsonify, hasKey, hasKeys } from '../utils/utils';
import { authorize } from '../auth';
import { devices_coll_str } from '../constants';

const { ObjectID } = mongodb;


function portNumbersToServiceName(ports: Array<string>, service_names: any) {
  return ports.map((element) => {
    const port_num = element.split('/')[0];
    if (hasKey(service_names, port_num)) {
      const transport_protocol = element.split('/')[1];
      return `${service_names[port_num]}/${transport_protocol}`
    } else {
      return element;
    }
  });
}


function verifyUpdateData(current_id: any, body: any) {
  const data = {...body};
  if (hasKey(data, '_id')) {
    data._id = new ObjectID(data._id);
    if (current_id.toString() !== data._id.toString()) return null;
  }
  return data;
}


// Device schema format:
//
// {
//   device: <Device name>,
//   device_model: <Device model>,
//   manufacturer: {
//     name: <Manufacturer name>,
//     website: <Manufacturer website>
//   },
//   domains: [<Which domain the device connects to>]
// }
function verifyInsertData(body: any) {
  const data = {...body};
  if (hasKey(data, '_id')) return null;
  if (!hasKeys(data, ['device', 'device_model', 'manufacturer', 'domains'])) return null;

  const manufacturer = data.manufacturer;
  if (!hasKeys(manufacturer, ['name', 'website'])) return null;

  return data;
}


export default async function device_api(db: any) {
  const api = express.Router();
  api.use(express.json());

  const service_names = JSON.parse(await fs.readFile('service-names-port-numbers.json', 'utf8'));
  const coll = db.collection(devices_coll_str);


  api.post(/^\/$/, authorize, jsonify(async (req: any, res: any) => {
    const data = verifyInsertData(req.body);
    if (!data) throw new BadRequestError('Document failed validation');

    const rv = await coll.insertOne(data);
    return rv.ops[0];
  }));


  api.post('/:id', authorize, jsonify(async (req: any, res: any) => {
    const query = {_id: new ObjectID(req.params.id)};
    const data = verifyUpdateData(query._id, req.body);
    if (!data) throw new BadRequestError('Document failed validation');

    // If the agent is trying to update the protocols then I have to convert
    // the port number to the service name. For example, 22/tcp to ssh/tcp.
    if (hasKey(data, 'protocols')) {
      data.protocols = portNumbersToServiceName(data.protocols, service_names);
    }

    const update: any = {$set: data};

    // Note that updateOne does not return the updated document this is
    // why I use findOneAndUpdate, but it requires a write lock for the
    // duration of the operation.
    const rv = await coll.findOneAndUpdate(query, update, {returnOriginal: false});
    if (!rv) throw new NotFoundError('Document does not exist');
    return rv.value;
  }));


  api.get(/^\/$/, jsonify(async () => {
    const rv = await coll.find({}).toArray();
    return rv;
  }));


  api.get('/:id', jsonify(async (req: any) => {
    const rv = await coll.findOne({_id: new ObjectID(req.params.id)});
    if (!rv) throw new NotFoundError('Document does not exist');
    return rv;
  }));


  return api;
}
