import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import path from 'path';
import logger from 'morgan';
import { getAmazonDocumentDB } from './db.js';

import device_api  from './routes/device.js';
import device_info_api from './routes/device_info.js';
import agent_api from './routes/agent.js';

const app = express();

(async () => {
  const amazon_document_db = await getAmazonDocumentDB();
  app.set('amazon_document_db', amazon_document_db);

  // Allow CORS on ExpressJS.
  if (app.get('env') === 'development') {
    // Note that cors_options is provided only for development mode.
    const cors_options = {
      credentials: true,
      origin: ['http://localhost:3000']
    };
    app.use(cors(cors_options));
  } else {
    app.use(cors());
  }
  app.options('*', cors());


  if (app.get('env') === 'production') {
    // If you have your node.js behind a proxy and are using secure: true,
    // you need to set "trust proxy" in express:
    app.set('trust proxy', 1);
  }


  app.use(helmet());
  app.use(logger('dev'));
  app.use(express.json());
  app.use(express.urlencoded({extended: true}));
  app.use(express.static('public'));


  app.use('/api/device', await device_api(amazon_document_db));
  app.use('/api/device_info', await device_info_api(amazon_document_db));
  app.use('/api/agent', await agent_api(amazon_document_db));

  app.get('*', (req, res) => {
    const curr_dirname = path.resolve();
    res.sendFile(path.join(curr_dirname, '/public', 'index.html'));
  });


  // catch 404 and forward to error handler
  app.use((req, res, next) => {
    const err: any = new Error('Not Found');
    err.status = 404;
    next(err);
  });


  // error handler
  app.use((err, req, res, next) => {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render('error');
  });
})();

export default app;
