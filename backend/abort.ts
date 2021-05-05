export default function abort(error, signame = 'SIGTERM') {
  if (typeof error !== 'undefined') {
    console.error('Aborting: ', error);
  }
  process.kill(process.pid, signame);
}
