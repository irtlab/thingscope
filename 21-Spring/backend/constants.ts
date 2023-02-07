import mongodb from 'mongodb';
import crypto from 'crypto';

// Amazon DocumentDB collections.
export const agents_coll_str = 'agents_coll';
export const auth_agents_coll_str = 'auth_agents_coll';
export const jwt_key_coll_str = 'jwt_key_coll';
export const devices_coll_str = 'devices_coll';

const { ObjectID } = mongodb;

// Bcrypt hashing algorithm's salt round.
export const salt_rounds = 10;

let unique_id = (new ObjectID()).toHexString();
export const jwt_access_secret_key = crypto.createHash('sha256').update(unique_id).digest('hex');
unique_id = (new ObjectID()).toHexString();
export const jwt_refresh_secret_key = crypto.createHash('sha256').update(unique_id).digest('hex');
