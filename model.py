from spendfrom import determine_db_dir

class Options(object):
    def __init__(self):
        self.fromaddresses = list()
        self.toaddress = None
        self.new = False
        self.datadir = determine_db_dir()
        self.conffile = "crown.conf"
        self.fee = "0.025"
        self.amount = None
        self.upto = None
        self.select = None
        self.passphrase = None
        self.pswdcanceled = False
        self.testnet = False
