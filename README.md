Orca's Home assignment
Author: Dor Mordechai

Because of the concurrency need, gunicorn is needed in this case.

Because the need for gunicorn, which also accepts sys.args, Argparse was clashing with
gunicorn arguments, so the workaround for this case is to set an environment variable
in the cmd run string `JSON_PATH=<orca_dir_path> `
Also, please run the code in the following way:



`PYTHONPATH=<orca_dir_path> JSON_PATH="<full_json_path>" gunicorn "server:app" --worker-class uvicorn.workers.UvicornH11Worker --preload -w 4 -t 2`

The need is to use with `gunicorn` in order to use `--preload` option.
But `gunicorn` isn't supported by fastAPI, so `uvicorn` workers are needed.