from flaskapp import app
import logging
from logging.config import dictConfig
import yaml


if __name__ == '__main__':

    with open("log_config.yaml", "r") as f: # 読み込み
        conf_file = yaml.safe_load(f.read()) # yaml.loadは使わない（脆弱性アリ）

        logging.config.dictConfig(conf_file) # 設定の完了
    #logging.config.fileConfig("log_config.yaml")
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5001)