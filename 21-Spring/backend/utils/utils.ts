// Returns a Promise that resolves after "ms" Milliseconds
export function sleep(ms: number) {
  return new Promise((res) => setTimeout(res, ms));
}


// Function checks if given object has a provided key/property or not.
//
// See ESLint rules for details:
// https://eslint.org/docs/rules/no-prototype-builtins
//
// Arguments:
// - object: JSON object.
// - key: Provide key, which will be checked.
//
// Returns true if an object has 'key' property, otherwise false.
export function hasKey(object, key) {
  const has = Object.prototype.hasOwnProperty;
  return has.call(object, String(key));
}


export function hasKeys(object: any, keys: Array<string>) {
  if (!keys.length) return false;

  for (let i = 0; i < keys.length; i++) {
    if (!hasKey(object, keys[i])) return false;
  }

  return true;
}


export const jsonify = (fn) => async (req, res, next) => {
  try {
    const rv = await fn(req, res, next);
    if (typeof rv !== 'undefined') res.json(rv);
  } catch (error) {
    const code = error.http_code || 500;
    const reason = error.http_reason || 'Internal Server Error';
    res.statusMessage = reason;
    res.status(code);
    res.json({
      code: code,
      reason: reason,
      message: error.message,
      ...(global && { stack: error.stack })
    });
  }
};
