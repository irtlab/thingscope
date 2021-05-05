import jwt from 'jsonwebtoken';
import mongodb from 'mongodb';
import crypto from 'crypto';
import { BadRequestError } from './errors';
import {
  auth_agents_coll_str,
  jwt_access_secret_key,
  jwt_refresh_secret_key
} from './constants';

const { ObjectID } = mongodb;


export function createKeyPairs() {
  const api_key = (new ObjectID()).toHexString();
  const unique_id = (new ObjectID()).toHexString();
  const secret_key = crypto.createHash('sha256').update(unique_id).digest('hex');

  return {api_key: api_key, secret_key: secret_key};
}


export function getAccessToken(payload: any, access_token_expires: string = '20m') {
  const options = {algorithm: 'HS256', expiresIn: access_token_expires};
  const access_token = jwt.sign(payload, jwt_access_secret_key, options);
  if (!access_token) throw new BadRequestError('Failed to generate access token');

  return access_token;
}


export function getRefreshToken(payload: any) {
  const options = {algorithm: 'HS256'};
  const refresh_token = jwt.sign(payload, jwt_refresh_secret_key, options);
  if (!refresh_token) throw new BadRequestError('Failed to generate refresh token');

  return refresh_token;
}


// Functions creates JWT tokens (access and refresh), stores them in MongoDB
// (collection name is auth_clients_coll) and returns a stored document.
//
// Arguments:
// -db: DB connection.
// -api_key: Agent's API KEY.
export async function initAuthentication(db: any, api_key: string) {
  const payload = {api_key: api_key, id: new ObjectID()};

  const access_token = getAccessToken(payload);
  const refresh_token = getRefreshToken(payload);

  const update = {
    $set: {
      createdAt: new Date(),
      api_key: api_key,
      refresh_token: refresh_token,
      access_token: access_token
    }
  };

  const coll = db.collection(auth_agents_coll_str);
  const query = {refresh_token: refresh_token};
  // Note that updateOne does not return the updated document this is
  // why I use findOneAndUpdate, but it requires a write lock for the
  // duration of the operation.
  const rv = await coll.findOneAndUpdate(query, update, {returnOriginal: false, upsert: true});

  return rv.value;
}


// Authorization Middleware.
export function authorize(req: any, res: any, next: any) {
  if (req.headers.authorization) {
    const access_token = req.headers.authorization;
    jwt.verify(access_token, jwt_access_secret_key, {algorithm: 'HS256'},
      (error: any, decoded_jwt: any) => {
        if (!error && decoded_jwt) {
          const db = req.app.get('amazon_document_db');
          const coll = db.collection(auth_agents_coll_str);
          const query = {$and: [{api_key: decoded_jwt.api_key}, {access_token: access_token}]};
          coll.findOne(query, (error: any, result: any) => {
            if (!error && result) {
              res.locals.jwt_data = decoded_jwt;
              next();
            } else {
              res.status(401).json({error: 'Authorization failed'});
            }
          });
        } else {
          res.status(401).json({error: 'Authorization failed'});
        }
      });
  } else {
    return res.redirect('/');
  }

  return null;
}
