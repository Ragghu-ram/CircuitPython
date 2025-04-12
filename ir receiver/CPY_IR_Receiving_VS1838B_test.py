import time
import board
import pulseio
import adafruit_irremote

# IR receiver setup on GPIO15
ir_receiver = pulseio.PulseIn(board.GP15, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

# Define IR remote codes and corresponding messages
REMOTE_CODES = { 
    "FF005DA2": "ON",
}

def decode_ir_signals(pulses):
    try:
        # Attempt to decode the received pulses
        codes = decoder.decode_bits(pulses)
        return codes
    except adafruit_irremote.IRNECRepeatException:
        print("IR repeat signal detected.")
        return None
    except adafruit_irremote.IRDecodeException:
        print("Failed to decode IR signal.")
        return None

while True:
    # Check if any pulses have been received
    pulses = decoder.read_pulses(ir_receiver)
    
    # Decode pulses to get the IR code
    received_code = decode_ir_signals(pulses)
    
    if received_code:
        # Convert the decoded bits to a hexadecimal string
        hex_code = ''.join(["%02X" % x for x in received_code])
        if hex_code in REMOTE_CODES:
            print(f"Button pressed: {REMOTE_CODES[hex_code]}")
        else:
            print(f"Unknown code: {hex_code}")
    
    # Small delay to prevent overwhelming the serial console
    time.sleep(0.2)
