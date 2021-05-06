export class HttpError extends Error {
  http_code;
  http_reason;
  constructor(message, code, reason) {
    super(message);
    this.http_code = code;
    this.http_reason = reason;
  }
}

export class BadRequestError extends HttpError {
  constructor(message, reason = 'Bad Request', code = 400) {
    super(message, code, reason);
  }
}

export class AuthorizationError extends HttpError {
  constructor(message, reason = 'Unauthorized', code = 401) {
    super(message, code, reason);
  }
}

export class NotFoundError extends HttpError {
  constructor(message, reason = 'Not Found', code = 404) {
    super(message, code, reason);
  }
}

export class ConflictError extends HttpError {
  constructor(message, reason = 'Conflict', code = 409) {
    super(message, code, reason);
  }
}
