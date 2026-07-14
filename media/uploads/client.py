import json
import time
import ctypes
from ctypes import c_int, c_char_p, CFUNCTYPE
from datetime import datetime
import requests

class EasyTestHttpClient:
    def __init__(self, server_base_url):
        self.server_url = server_base_url.rstrip('/')
        self.device_connected = False
        self.connection_in_progress = False

        possible_paths = [
            "./resources/EasyTestSDK_x64.dll",
            "../resources/EasyTestSDK_x64.dll",
            "../../resources/EasyTestSDK_x64.dll",
            "./EasyTestSDK_x64.dll",
            "../EasyTestSDK_x64.dll"
        ]

        self.lib = None
        for path in possible_paths:
            try:
                self.lib = ctypes.CDLL(path)
                print(f"✅ Found EasyTest SDK at: {path}")
                break
            except OSError:
                continue

        if self.lib is None:
            raise FileNotFoundError("EasyTestSDK_x64.dll not found in any expected location")

        self._setup_callbacks()
        self._define_functions()
        self._register_callbacks()

        self.lib.License(1, b"SUNARS2013")
        self.lib.SetLogOn(0)

    def _setup_callbacks(self):
        self._connect_cb = CFUNCTYPE(None, c_int, c_int, c_char_p)(self._on_connect)
        self._vote_cb = CFUNCTYPE(None, c_int, c_int, c_char_p)(self._on_vote)
        self._key_cb = CFUNCTYPE(None, c_int, c_int, c_char_p, c_int, ctypes.c_float, c_char_p)(self._on_key)
        self._hd_cb = CFUNCTYPE(None, c_int, c_int, c_char_p)(self._on_hd_param)
        self._keypad_cb = CFUNCTYPE(None, c_int, c_int, c_char_p, c_int, c_char_p)(self._on_keypad_param)

    def _define_functions(self):
        self.lib.License.argtypes = [c_int, c_char_p]
        self.lib.License.restype = c_int

        self.lib.Connect.argtypes = [c_int, c_char_p]
        self.lib.Connect.restype = c_int

        self.lib.Disconnect.argtypes = [c_int]
        self.lib.Disconnect.restype = c_int

        self.lib.VoteStart2.argtypes = [c_int, c_int, c_char_p]
        self.lib.VoteStart2.restype = c_int

        self.lib.VoteStop2.argtypes = [c_int]
        self.lib.VoteStop2.restype = c_int

        self.lib.SetLogOn.argtypes = [c_int]
        self.lib.SetLogOn.restype = c_int

        self.lib.SetConnectEventCallBack.argtypes = [type(self._connect_cb)]
        self.lib.SetHDParamEventCallBack.argtypes = [type(self._hd_cb)]
        self.lib.SetKeypadParamEventCallBack.argtypes = [type(self._keypad_cb)]
        self.lib.SetVoteEventCallBack.argtypes = [type(self._vote_cb)]
        self.lib.SetKeyEventCallBack.argtypes = [type(self._key_cb)]

    def _register_callbacks(self):
        self.lib.SetConnectEventCallBack(self._connect_cb)
        self.lib.SetVoteEventCallBack(self._vote_cb)
        self.lib.SetKeyEventCallBack(self._key_cb)
        self.lib.SetHDParamEventCallBack(self._hd_cb)
        self.lib.SetKeypadParamEventCallBack(self._keypad_cb)

    def _post_event(self, endpoint, data):
        url = f"{self.server_url}/api/{endpoint}/create/"
        try:
            for attempt in range(3):
                response = requests.post(url, json=data, timeout=5)
                if response.status_code == 201:
                    print(f"✅ Event posted to {endpoint}")
                    return True
                else:
                    print(f"❌ Failed to post event to {endpoint}: {response.status_code} {response.text}")
                time.sleep(1)
            print(f"❌ Giving up posting event to {endpoint} after retries.")
        except Exception as e:
            print(f"❌ HTTP post error to {endpoint}: {e}")

    def _on_connect(self, base_id, mode, info):
        info_str = info.decode() if info else ""
        print(f"🔌 Device Connect: BaseID={base_id}, Mode={mode}, Info={info_str}")

        if info_str == "1":
            self.device_connected = True
            print("🚀 Auto-starting vote session...")
            self.start_vote(base_id, 10, "1,1,0,0,4,1")
        else:
            self.device_connected = False

        event = {
            'base_id': base_id,
            'mode': mode,
            'info': info_str,
            'timestamp': datetime.now().isoformat(),
        }
        self._post_event('connect-events', event)

    def _on_vote(self, base_id, mode, info):
        info_str = info.decode() if info else ""
        print(f"🗳️ Vote Event: BaseID={base_id}, Mode={mode}, Info={info_str}")

        event = {
            'base_id': base_id,
            'mode': mode,
            'info': info_str,
            'timestamp': datetime.now().isoformat(),
        }
        self._post_event('vote-events', event)

    def _on_key(self, base_id, key_id, key_sn, mode, timestamp, info):
        key_sn_str = key_sn.decode() if key_sn else ""
        info_str = info.decode() if info else ""
        print(f"🔑 Key Event: BaseID={base_id}, KeyID={key_id}, KeySN={key_sn_str}, Mode={mode}, Time={timestamp}, Info={info_str}")

        event = {
            'base_id': base_id,
            'key_id': key_id,
            'key_sn': key_sn_str if key_sn_str else "unknown",
            'mode': mode,
            'timestamp': datetime.now().isoformat(),
            'info': info_str,
            'client_timestamp': datetime.now().isoformat(),
            'event_type': 'real_hardware',
        }
        self._post_event('key-events', event)

    def _on_hd_param(self, base_id, mode, info):
        info_str = info.decode() if info else ""
        print(f"📊 HD Param: BaseID={base_id}, Mode={mode}, Info={info_str}")

        event = {
            'base_id': base_id,
            'mode': mode,
            'info': info_str,
            'timestamp': datetime.now().isoformat(),
        }
        self._post_event('hd-param-events', event)

    def _on_keypad_param(self, base_id, key_id, key_sn, mode, info):
        key_sn_str = key_sn.decode() if key_sn else ""
        info_str = info.decode() if info else ""
        print(f"⌨️ Keypad Param: BaseID={base_id}, KeyID={key_id}, KeySN={key_sn_str}, Mode={mode}, Info={info_str}")

        event = {
            'base_id': base_id,
            'key_id': key_id,
            'key_sn': key_sn_str,
            'mode': mode,
            'info': info_str,
            'timestamp': datetime.now().isoformat(),
        }
        self._post_event('keypad-param-events', event)

    def connect_device(self, conn_type=2, conn_str=""):
        if self.connection_in_progress or self.device_connected:
            print("⚠️ Connection already in progress or device already connected")
            return 0
        self.connection_in_progress = True

        print(f"🔌 Connecting to device (type={conn_type})...")
        result = self.lib.Connect(conn_type, conn_str.encode())
        if result == 0:
            print("✅ Device connection initiated")
        else:
            print(f"❌ Device connection failed with code: {result}")
            self.connection_in_progress = False
        return result

    def disconnect_device(self, base_id=0):
        return self.lib.Disconnect(base_id)

    def start_vote(self, base_id=0, vote_type=10, config="1,1,0,0,4,1"):
        return self.lib.VoteStart2(base_id, vote_type, config.encode())

    def stop_vote(self, base_id=0):
        return self.lib.VoteStop2(base_id)

def main():
    SERVER_BASE = "http://172.50.4.138:8000"  # or your LAN IP if different machine
    print("🚀 Starting EasyTest HTTP Client...")
    client = EasyTestHttpClient(SERVER_BASE)

    try:
        print("🔌 Connecting to EasyTest device...")
        result = client.connect_device(conn_type=2, conn_str="")
        if result != 0:
            print("🔄 Network auto-discovery failed, trying USB...")
            result = client.connect_device(conn_type=1, conn_str="")

        if result != 0:
            print("❌ Hardware connection failed! Check power/drivers.")
        else:
            print("⏳ Device connected. Awaiting SDK events...")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down client...")

    finally:
        client.disconnect_device()
        print("🪜 Cleanup done.")

if __name__ == "__main__":
    main()
