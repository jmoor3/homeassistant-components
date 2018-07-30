import crc8
import logging
import socket
import time

from threading import Lock

LOGGER = logging.getLogger(__name__)

class SpaClient:
    def __init__(self, socket):
        self.s = socket
        self.light = None
        self.current_temp = None
        self.hour = None
        self.minute = None
        self.heating_mode = ""
        self.temp_scale = ""
        self.temp_range = ""
        self.pump1 = ""
        self.pump2 = ""
        self.set_temp = None
        self.priming = False
        self.time_scale = "12 Hr"
        self.heating = False
        self.circ_pump = False
        time.sleep(2)
        self.read_all_msg()

    s = None
    ip = None
    l = Lock()

    @staticmethod
    def get_socket(host_ip = None):
        if (host_ip):
            SpaClient.ip = host_ip
        if SpaClient.s is None:
            SpaClient.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SpaClient.s.connect((SpaClient.ip, 4257))
            SpaClient.s.setblocking(0)
        return SpaClient.s

    def reconnect_socket():
        SpaClient.s = None
        return SpaClient.get_socket()

    def handle_status_update(self, byte_array):
        self.current_temp = byte_array[2]
        self.priming = byte_array[1] & 0x01 == 1

        self.hour = byte_array[3]
        self.minute = byte_array[4]
        self.heating_mode = \
            ("Ready", "Rest", "Ready in Rest")[byte_array[5]]
        flag3 = byte_array[9]
        self.temp_scale = "Farenheit" if (flag3 & 0x01 == 0) else "Celcius"
        self.time_scale = "12 Hr" if (flag3 & 0x02 == 0) else "24 Hr"
        flag4 = byte_array[10]
        self.heating = flag4 & 0x30
        self.temp_range = "Low" if (flag4 & 0x04 == 0) else "High"
        pump_status = byte_array[11]
        self.pump1 = ("Off", "Low", "High")[pump_status & 0x03]
        self.pump2 = ("Off", "Low", "High")[pump_status & 0x12]
        self.circ_pump = byte_array[13] & 0x02 == 1
        self.light = byte_array[14] & 0x03 == 0x03
        self.set_temp = byte_array[20]

    def get_set_temp(self):
        return self.set_temp

    def get_pump(self, pump_num):
        if pump_num == 1:
            return self.get_pump1()
        return self.get_pump2()

    def get_pump1(self):
        return self.pump1

    def get_pump2(self):
        return self.pump2

    def get_temp_range(self):
        return self.temp_range

    def get_current_time(self):
        return "%d:%02d" % (self.hour, self.minute)

    def get_light(self):
        return self.light

    def get_current_temp(self):
        return self.current_temp

    def string_status(self):
        s = ""
        s = s + "Temp: %d, Set Temp: %d, Time: %d:%02d\n" % \
            (self.current_temp, self.set_temp, self.hour, self.minute)
        s = s + "Priming: %s, Heating Mode: %s Temp Scale: %s, Time Scale: %s\n" % \
            (self.priming, self.heating_mode, self.temp_scale, self.time_scale)
        s = s + "Heating: %s, Temp Range: %s, Pump1: %s, Pump2: %s, Circ Pump: %s, Light: %s\n" % \
            (self.heating, self.temp_range, self.pump1, self.pump2, self.circ_pump, self.light)
        return s

    def compute_checksum(self, len_bytes, bytes):
        hash = crc8.crc8()
        hash._sum = 0x02
        hash.update(len_bytes)
        hash.update(bytes)
        checksum = hash.digest()[0]
        checksum = checksum ^ 0x02
        return checksum

    def read_msg(self):
        SpaClient.l.acquire()
        try:
            len_chunk = SpaClient.s.recv(2)
        except OSError as e:
            SpaClient.l.release()
            return False

        if len_chunk == b'' or len(len_chunk) == 0:
            return False
        length = len_chunk[1]
        if int(length) == 0:
            SpaClient.l.release()
            return False

        try:
            chunk = SpaClient.s.recv(length)
        except BaseException as e:
            LOGGER.error("Failed to receive: len_chunk: %s, error: %s",
                         len_chunk, e)
            SpaClient.l.release()
            return False

        SpaClient.l.release()

        # Status update prefix
        if chunk[0:3] == b'\xff\xaf\x13':
            # print("Status Update")
            self.handle_status_update(chunk[3:])

        return True

    def read_all_msg(self):
        while (self.read_msg()):
            True

    def send_message(self, type, payload):
        length = 5 + len(payload)
        checksum = self.compute_checksum(bytes([length]), type + payload)
        prefix = b'\x7e'
        message = prefix + bytes([length]) + type + payload + \
            bytes([checksum]) + prefix

        try:
            SpaClient.s.send(message)
        except IOError as e:
            LOGGER.error("Lost connection, error: %s", e)
            SpaClient.s = SpaClient.reconnect_socket()
            SpaClient.s.send(message)

    def send_config_request(self):
        self.send_message(b'\x0a\xbf\x04', bytes([]))

    def send_toggle_message(self, item):
        # 0x04 - pump 1
        # 0x05 - pump 2
        # 0x11 - light 1
        # 0x51 - heating mode
        # 0x50 - temperature range

        self.send_message(b'\x0a\xbf\x11', bytes([item]) + b'\x00')

    def set_temperature(self, temp):
        self.set_temp = int(temp)
        self.send_message(b'\x0a\xbf\x20', bytes([int(temp)]))

    def set_light(self, value):
        if self.light == value:
            return
        self.send_toggle_message(0x11)
        self.light = value

    def set_pump(self, pump_num, value):
        pump_val = self.pump1
        pump_code = 0x04
        if pump_num == 2:
            pump_val = self.pump2
            pump_code = 0x05
        if pump_val == value:
            return
        if value == "High" and pump_val == "Off":
            self.send_toggle_message(pump_code)
            self.send_toggle_message(pump_code)
        elif value == "Off" and pump_val == "Low":
            self.send_toggle_message(pump_code)
            self.send_toggle_message(pump_code)
        else:
            self.send_toggle_message(pump_code)
        if pump_num == 1:
            self.pump1 = value
        else:
            self.pump2 = value


#import time
#sc = SpaClient(SpaClient.get_socket('192.168.0.150'))
#time.sleep(2)
#sc.read_all_msg()
#print(sc.string_status())
#sc.send_config_request()
#sc.send_toggle_message(0x11)
#sc.set_temperature(97)
#time.sleep(2)
#sc.read_all_msg()
#print(sc.string_status())
#sc.send_toggle_message(0x11) #light
#send_toggle_message(0x04) #pump1
#send_toggle_message(0x05) #light
