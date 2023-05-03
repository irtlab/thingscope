import express from 'express';
import { BadRequestError } from '../utils/errors.js';
import { jsonify, hasKey } from '../utils/utils.js';
import { devices_coll_str } from '../constants.js';


export default async function device_info_api(db: any) {
  const api = express.Router();
  api.use(express.json());

  const coll = db.collection(devices_coll_str);

  api.get(/^\/$/, jsonify(async (req: any) => {
    if (!hasKey(req.query, 'device')) throw new BadRequestError('Request failed validation');
    if (!req.query.device) throw new BadRequestError('Device name is not provided');

    // TODO I should find a way to query data based on regexp match.
    const rv = await coll.find({}).toArray();

    const regexp = new RegExp(req.query.device.toLowerCase(), 'g');
    const result = rv
      .filter((element: any) => (element.device.toLowerCase()).match(regexp))
      .map((obj: any) => ({device: obj.device, privacy_policy: obj.privacy_policy ? obj.privacy_policy : ''}));

    return result;
  }));


  return api;
}
