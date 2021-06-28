''' 
create by renjch 
2021-06-28
'''

from evdev import InputDevice, ecodes, list_devices, categorize
import signal, sys
from select import select
import time


class Barcode_Scanner:

    scancodes = {
    # Scancode: ASCIICode
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
        20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
        40: u'\'', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
        50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }

    scancodes_shift = {
    # scancodes_shift: ASCIICode
        0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
        10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
        30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
        40: u'"', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
        50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }

    '''
    "Datalogic ADC, Inc. Handheld Barcode Scanner"
    '''
    def __init__(self, device_name):
        self.barCodeDeviceString = device_name
        self.dev = None

        for i in range(10):
            devices = map(InputDevice, list_devices())
            for device in devices:
                if device.name == self.barCodeDeviceString:
                    self.dev = InputDevice(device.fn)
                    print(device_name + ' founded.')
                    return
            print(device_name + ' founded. Try again ... ')
            time.sleep(2)      

        if not self.dev:
            raise RuntimeError(device_name + ' not found!')

    def detectInputKey(self):
        if not self.dev:
            raise RuntimeError(device_name + ' not found!')
        
        end_flag = False
        str_val = ''
        key_stack = []
        shift_status = False 
        
        while not end_flag:    
            select([self.dev], [], [])
            for event in self.dev.read():
                if event.code == 0:
                    continue

                if event.code in Barcode_Scanner.scancodes.keys():
                    if event.value == 1: # key down
                        key_stack.append(event.code)
                        if event.code in [42, 54]: # shift pressed
                            #print('shift pressed')
                            shift_status = True

                    elif event.value == 0: # key up
                        try:
                            idx = key_stack.index(event.code)
                            if event.code not in [42, 54, 28]: # not shift or CRLF
                                code = Barcode_Scanner.scancodes_shift[event.code] if shift_status else Barcode_Scanner.scancodes[event.code]
                                str_val += code
                            key_stack.pop(idx)
                            if event.code in [42, 54]:
                                #print('shift up')
                                shift_status = False
                        except IndexError as e:
                            print('except', e)

                    if event.code == 28 and event.value == 0: # enter key up
                        end_flag = True
                        break

        return str_val



if __name__ == '__main__':
    ''' you need to confirm the device name '''
    scanner = Barcode_Scanner('Datalogic ADC, Inc. Handheld Barcode Scanner')
    while True:
        ret = scanner.detectInputKey()
        print("-----------------------------")
        print(ret)
        print("-----------------------------")

