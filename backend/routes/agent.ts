import express from 'express';
import mongodb from 'mongodb';
import { initAuthentication, createKeyPairs, getAccessToken } from '../auth';
import { BadRequestError, NotFoundError } from '../utils/errors';
import { jsonify, hasKey, hasKeys } from '../utils/utils';
import { agents_coll_str, auth_agents_coll_str } from '../constants';


async function setupAgentAuthColl(db: any) {
  await db.createCollection(auth_agents_coll_str);
  const coll = db.collection(agents_coll_str);
  await coll.createIndex({createdAt: 1}, {expireAfterSeconds: 1200});
}


function getAgentSchema() {
  const keys = createKeyPairs();
  const agent_schema = {
    created: new Date(),
    last_update: new Date(),
    api_key: keys.api_key,
    secret_key: keys.secret_key
  };

  return agent_schema;
}


function verifySignIn(body: any) {
  if (!hasKeys(body, ['api_key', 'secret_key']) || hasKey(body, '_id')) return null;
  return {api_key: body.api_key.trim(), secret_key: body.secret_key.trim()};
}


export default async function agent_api(db: any) {
  const api = express.Router();
  api.use(express.json());

  // await setupAgentAuthColl(db);

  const coll = db.collection(agents_coll_str);
  const { ObjectID } = mongodb;


  api.post(/^\/$/, jsonify(async (req: any, res: any) => {
    // TODO: Currently this is public API but this should be private later.
    const agent_schema = getAgentSchema();
    await coll.insertOne(agent_schema);
    return {message: 'ok'};
  }));


  api.post('/sign_in', jsonify(async (req: any, res: any) => {
    const data: any = verifySignIn(req.body);
    if (!data) throw new BadRequestError('Request failed validation');

    const query = {api_key: data.api_key, secret_key: data.secret_key};
    const found = await coll.findOne(query);
    if (!found) return new BadRequestError('Sign In failed. Wrong api and/or secret key.');

    const user_data = await initAuthentication(db, data.api_key);
    return user_data;
  }));


  api.get('/:id/sign_out', jsonify(async (req: any, res: any) => {
    if (req.headers.authorization) {
      const auth = JSON.parse(req.headers.authorization);
      const auth_coll = db.collection(auth_agents_coll_str);
      await auth_coll.deleteOne({
        $or: [{access_token: auth.access_token}, {refresh_token: auth.refresh_token}]
      });
    }

    res.status(200).end();
  }));


  api.post('/:id/update_access_token', jsonify(async (req: any) => {
    if (!req.body.refresh_token) throw new BadRequestError('Request failed validation');

    const auth_coll = db.collection(auth_agents_coll_str);
    const query = {
      $and: [{refresh_token: req.body.refresh_token}, {api_key: req.params.id}]
    };
    const found = await auth_coll.findOne(query);
    if (!found) throw new NotFoundError('Token not found');

    const update = {
      $set: {
        createdAt: new Date(),
        access_token: getAccessToken({api_key: req.params.id, id: new ObjectID()})
      }
    };

    const rv = await auth_coll.findOneAndUpdate(query, update, {returnOriginal: false});
    return rv.value;
  }));


  return api;
}
