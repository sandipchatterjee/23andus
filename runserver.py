#!/usr/bin/env python3

import os
from twentythreeandus import app

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret_key_string' ## should pull this from environment in future
    app.run(host='0.0.0.0', port=8888, debug=True)
