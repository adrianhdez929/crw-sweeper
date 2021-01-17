#!/usr/bin/env python3
#
# Use the raw transactions API to spend crowns received on particular addresses,
# and send any change back to that same address.
#
# Assumes it will talk to a crownd or Crown-Qt running
# on localhost.
#
# Depends on bitcoinrpc
#

from decimal import *
import math
import os
import os.path
import platform
import sys
import time
from bitcoinrpc.authproxy import AuthServiceProxy, json, JSONRPCException

BASE_FEE=Decimal("0.001")
verbosity = 0

class SpendFrom(object):
    def __init__(self, dialog=None):
        self.dialog = dialog

    def check_json_precision(self):
        """Make sure json library being used does not lose precision converting BTC values"""
        n = Decimal("20000000.00000003")
        satoshis = int(json.loads(json.dumps(float(n)))*1.0e8)
        if satoshis != 2000000000000003:
            raise RuntimeError("JSON encode/decode loses precision")
    
    @staticmethod
    def determine_db_dir():
        """Return the default location of the crown data directory"""
        if platform.system() == "Darwin":
            return os.path.expanduser("~/Library/Application Support/Crown/")
        elif platform.system() == "Windows":
            return os.path.join(os.environ['APPDATA'], "Crown")
        return os.path.expanduser("~/.crown")

    def read_bitcoin_config(self, dbdir, conffile):
        """Read the crown config file from dbdir, returns dictionary of settings"""
        with open(os.path.join(dbdir, conffile)) as stream:
            config = dict(line.strip().split('=', 1) for line in stream if not line.startswith("#") and not len(line.strip()) == 0)
        #print("Leaving read_bitcoin_config with %s and %s"%(config['rpcuser'], config['rpcpassword']))
        return config

    def connect_JSON(self, config):
        """Connect to a crown JSON-RPC server"""
        testnet = config.get('testnet', '0')
        testnet = (int(testnet) > 0)  # 0/1 in config file, convert to True/False
        if not 'rpcport' in config:
            config['rpcport'] = 19341 if testnet else 9341
        connect = "http://%s:%s@127.0.0.1:%s"%(config['rpcuser'], config['rpcpassword'], config['rpcport'])
        try:
            result = AuthServiceProxy(connect, timeout=600)
            # ServiceProxy is lazy-connect, so send an RPC command mostly to catch connection errors,
            # but also make sure the crownd we're talking to is/isn't testnet:
            if result.getmininginfo()['testnet'] != testnet:
                self.dialog.notify("RPC server at "+connect+" testnet setting mismatch\n")
                raise Exception
            return result
        except:
            self.dialog.notify("Error connecting to RPC server at "+connect+"\n")
            raise Exception

    def unlock_wallet(self, crownd, passphrase):
        info = crownd.getinfo()
        if 'unlocked_until' not in info:
            return True # wallet is not encrypted
        t = int(info['unlocked_until'])
        if t <= time.time():
            try:
                crownd.walletpassphrase(passphrase, 5)
            except:
                self.dialog.notify("Please enter your passphrase\n")

        info = crownd.getinfo()
        return int(info['unlocked_until']) > time.time()

    def list_available(self, crownd):
        address_summary = dict()

        address_to_account = dict()
        for info in crownd.listreceivedbyaddress(0):
            address_to_account[info["address"]] = info["account"]

        unspent = crownd.listunspent(0)
        for output in unspent:
            # listunspent doesn't give addresses, so:
            rawtx = crownd.getrawtransaction(output['txid'], 1)
            vout = rawtx["vout"][output['vout']]
            pk = vout["scriptPubKey"]

            # This code only deals with ordinary pay-to-crown-address
            # or pay-to-script-hash outputs right now; anything exotic is ignored.
            if pk["type"] != "pubkeyhash" and pk["type"] != "scripthash":
                continue

            address = pk["addresses"][0]
            if address in address_summary:
                address_summary[address]["total"] += vout["value"]
                address_summary[address]["outputs"].append(output)
            else:
                address_summary[address] = {
                    "total" : vout["value"],
                    "outputs" : [output],
                    "account" : address_to_account.get(address, "")
                    }

        return address_summary

    def select_coins(self, needed, inputs, criteria):
        # criteria will be used to prioritise the coins selected for this txn.
        # Some alternative strategies are oldest|smallest|largest UTXO first.
        # Using smallest first will combine the largest number of UTXOs but may 
        # produce a transaction which is too large. The input set is an unordered
        # list looking something like
        # [{'vout': 1, 'address': 'tCRWTQhoMTQgyHZyrhZSnScJYuGXCHXPKdNwd', 'confirmations': 12086, 'spendable': True, 'amount': Decimal('0.92500000'), 'scriptPubKey': '76a9149e2b5779df2364dc833fd5167bc561ce65f3884b88ac', 'txid': 'ef4d44dc28b818eb09651f1e62f348aa66a81b6e2baf5242ba4f48ab68a78aca', 'account': 'XMN05'}, 
        #  {'vout': 1, 'address': 'tCRWTQhoMTQgyHZyrhZSnScJYuGXCHXPKdNwd', 'confirmations': 5906, 'spendable': True, 'amount': Decimal('0.92500000'), 'scriptPubKey': '76a9149e2b5779df2364dc833fd5167bc561ce65f3884b88ac', 'txid': 'c1142434fa1fb3484bd54b42fd654fe86a7c2de9ec62f049b868db1439b591ca', 'account': 'XMN05'}, 
        #  {'vout': 0, 'address': 'tCRWTQhoMTQgyHZyrhZSnScJYuGXCHXPKdNwd', 'confirmations': 1395, 'spendable': True, 'amount': Decimal('0.75000000'), 'scriptPubKey': '76a9149e2b5779df2364dc833fd5167bc561ce65f3884b88ac', 'txid': '74205c8acdfeffb57fba501676e7ae14fff4a6dc06843ad008eb841f7ae198ca', 'account': 'XMN05'}, 
        #  {'vout': 0, 'address': 'tCRWTQhoMTQgyHZyrhZSnScJYuGXCHXPKdNwd', 'confirmations': 9531, 'spendable': True, 'amount': Decimal('0.75000000'), 'scriptPubKey': '76a9149e2b5779df2364dc833fd5167bc561ce65f3884b88ac', 'txid': 'f5c19fe103d72e9257a54e3562a85a6d6309d8a0d419aee7228a2c69e02e9cca', 'account': 'XMN05'}
        #  ...
        outputs = []
        have = Decimal("0.0")
        n = 0
        if verbosity > 0: print("Selecting coins from the set of %d inputs"%len(inputs))
        if verbosity > 1: print(inputs)
        while have < needed and n < len(inputs) and n < 1660:
            outputs.append({ "txid":inputs[n]["txid"], "vout":inputs[n]["vout"]})
            have += inputs[n]["amount"]
            n += 1
        if verbosity > 0: print("Chose %d UTXOs with total value %f CRW requiring %f CRW change"%(n, have, have-needed)) 
        if verbosity > 2: print(outputs)   
        return (outputs, have-needed)

    def create_tx(self, crownd, fromaddresses, toaddress, amount, fee, criteria, upto):
        all_coins = self.list_available(crownd)

        total_available = Decimal("0.0")
        needed = amount+fee
        potential_inputs = []
        for addr in fromaddresses:
            if addr not in all_coins:
                continue
            potential_inputs.extend(all_coins[addr]["outputs"])
            total_available += all_coins[addr]["total"]

        if total_available == 0:
            self.dialog.notify("Selected addresses are empty\n")
            return
        elif total_available < needed:
            if upto:
                needed = total_available
                amount = total_available - fee
                print("Warning, only %f CRW available, sending up to %f CRW"%(total_available, amount))
            else:
                self.dialog.notify("Error, only %f CRW available, need %f CRW\n"%(total_available, needed))
                return
            
        #
        # Note:
        # Python's json/jsonrpc modules have inconsistent support for Decimal numbers.
        # Instead of wrestling with getting json.dumps() (used by jsonrpc) to encode
        # Decimals, I'm casting amounts to float before sending them to crownd.
        #
        outputs = { toaddress : float(amount) }
        (inputs, change_amount) = self.select_coins(needed, potential_inputs, criteria)
        if change_amount < 0:         # hit the transaction UTXO limit
            amount += change_amount
            outputs[toaddress] = float(amount)
            if not upto:
                self.dialog.notify("Error, only %f CRW available, need %f\n"%(amount + fee, needed))
                return
        elif change_amount > BASE_FEE:  # don't bother with zero or tiny change
            change_address = fromaddresses[-1]
            if change_address in outputs:
                outputs[change_address] += float(change_amount)
            else:
                outputs[change_address] = float(change_amount)

        rawtx = crownd.createrawtransaction(inputs, outputs)
        signed_rawtx = crownd.signrawtransaction(rawtx)
        if not signed_rawtx["complete"]:
            self.dialog.notify("signrawtransaction failed\n")
            return
        txdata = signed_rawtx["hex"]

        return txdata

    def compute_amount_in(self, crownd, txinfo):
        result = Decimal("0.0")
        for vin in txinfo['vin']:
            in_info = crownd.getrawtransaction(vin['txid'], 1)
            vout = in_info['vout'][vin['vout']]
            result = result + vout['value']
        return result

    def compute_amount_out(self, txinfo):
        result = Decimal("0.0")
        for vout in txinfo['vout']:
            result = result + vout['value']
        return result

    def sanity_test_fee(self, crownd, txdata_hex, max_fee, fee):
        class FeeError(RuntimeError):
            pass
        try:
            txinfo = crownd.decoderawtransaction(txdata_hex)
            total_in = self.compute_amount_in(crownd, txinfo)
            total_out = self.compute_amount_out(txinfo)
            if total_in-total_out > max_fee:
                raise FeeError("Rejecting transaction, unreasonable fee of "+str(total_in-total_out))

            tx_size = len(txdata_hex)/2
            kb = tx_size/1000  # integer division rounds down
            if kb > 1 and fee < BASE_FEE:
                raise FeeError("Rejecting no-fee transaction, larger than 1000 bytes")
            if total_in < 0.01 and fee < BASE_FEE:
                raise FeeError("Rejecting no-fee, tiny-amount transaction")
            # Exercise for the reader: compute transaction priority, and
            # warn if this is a very-low-priority transaction

        except FeeError as err:
            self.dialog.notify((str(err)+"\n"))
            return
