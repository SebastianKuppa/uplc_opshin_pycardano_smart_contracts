import gift
import pycardano
from opshin.prelude import *
from pycardano import PlutusV2Script, plutus_script_hash, Network, Address

import utils


GLOBAL_network = Network.TESTNET


def create_script_address(cbor_file="./build/gift/script.cbor"):
    with open(cbor_file, "r") as f:
        script_hex = f.read()
    gift_script = PlutusV2Script(bytes.fromhex(script_hex))
    script_hash = plutus_script_hash(gift_script)
    script_address = Address(script_hash, network=GLOBAL_network)

    return script_address


def run_gift_contract():
    # create smart contract address
    gift_script_address = create_script_address()
    # load giver and receiver addresses
    giver_skey = pycardano.PaymentSigningKey.load("./keys/giver/payment.skey")
    giver_vkey = pycardano.PaymentVerificationKey.load("./keys/giver/payment.vkey")
    giver_address = Address(giver_vkey.hash(), network=utils.GLOBAL_network)

    taker_skey = pycardano.PaymentSigningKey.load("./keys/taker/payment.skey")
    taker_vkey = pycardano.PaymentVerificationKey.load("./keys/taker/payment.vkey")
    taker_address = Address(taker_vkey.hash(), network=utils.GLOBAL_network)

    # build transaction for sending funds and datum to script address
    builder = pycardano.TransactionBuilder(context=utils.GLOBAL_context)
    # add giver address as transaction input
    builder.add_input_address(giver_address)

    # init datum
    datum = gift.CancelDatum(taker_vkey.hash().to_primitive())
    # add gift_script as transaction output
    builder.add_output(pycardano.TransactionOutput(gift_script_address,
                                                   5_000_000,
                                                   datum_hash=pycardano.datum_hash(datum)))
    # sign the script transaction


if __name__ == "__main__":
    run_gift_contract()