from src import config, base

if __name__ == "__main__":
    gconfig = config.Config()
    base = base.Base(gconfig)
    base.run()
