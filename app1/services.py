# import ctypes
# import threading
# import time
# from ctypes import c_int, c_char_p, c_void_p, POINTER, CFUNCTYPE
# from django.utils import timezone
# from django.db import transaction
# from .models import Device, KeypadEvent, VoteSession
# from core.easy_test import EasyTest
# import logging

# logger = logging.getLogger(__name__)

# class DjangoEasyTestHandler(EasyTest):
#     def __init__(self):
#         super().__init__()
#         self.running = False
#         self.connection_attempts = 0
#         self.max_connection_attempts = 5

#     def _on_connect(self, base_id, mode, info):
#         super()._on_connect(base_id, mode, info)
#         logger.info(f"📡 Device Connected: ID={base_id}, Mode={mode.decode()}, Info={info.decode()}")
        
#         try:
#             with transaction.atomic():
#                 device, created = Device.objects.get_or_create(
#                     base_id=base_id,
#                     defaults={
#                         'mode': mode.decode() if mode else '',
#                         'info': info.decode() if info else '',
#                         'status': 'connected'
#                     }
#                 )
                
#                 if not created:
#                     device.mode = mode.decode() if mode else ''
#                     device.info = info.decode() if info else ''
#                     device.status = 'connected'
#                     device.save()
                
#                 # Auto-start vote if info is "1"
#                 if info.decode() == "1":
#                     logger.info(f"Auto-starting vote for device {base_id}")
#                     self.vote_start(0, 10, "1,1,0,0,4,1")
                    
#                     VoteSession.objects.create(
#                         device=device,
#                         session_id=0,
#                         duration=10,
#                         config="1,1,0,0,4,1",
#                         status='active'
#                     )
                    
#                 logger.info(f"Device {base_id} {'created' if created else 'updated'} in database")
                
#         except Exception as e:
#             logger.error(f"Error handling device connection: {e}")

#     def _on_key(self, base_id, key_id, key_sn, mode, timestamp, info):
#         key_sn_str = key_sn.decode() if key_sn else ''
#         info_str = info.decode().strip() if info else ''
#         mode_str = info.decode() if mode else ''

#         logger.info(f"🧭 Keypad Event: BaseID={base_id}, KeyID={key_id}, SN={key_sn_str}, Info={repr(info_str)}, Time={timestamp}")

#         try:
#             with transaction.atomic():
#                 device = Device.objects.get(base_id=base_id)
                
#                 KeypadEvent.objects.create(
#                     device=device,
#                     key_id=key_id,
#                     key_sn=key_sn_str,
#                     mode=mode_str,
#                     timestamp=timestamp,
#                     info=info_str,
#                     processed=False
#                 )
                
#                 logger.info(f"Keypad event saved for device {base_id}")
                
#         except Device.DoesNotExist:
#             logger.error(f"Device with base_id {base_id} not found in database")
#         except Exception as e:
#             logger.error(f"Error saving keypad event: {e}")

#     def connect_with_retry(self, base_id, mode):
#         """Try to connect with retry logic"""
#         for attempt in range(self.max_connection_attempts):
#             try:
#                 logger.info(f"Connection attempt {attempt + 1}/{self.max_connection_attempts}")
#                 result = self.connect(base_id, mode)
#                 if result:  # Assuming connect returns True on success
#                     logger.info("Connection successful!")
#                     return True
#                 else:
#                     logger.warning(f"Connection attempt {attempt + 1} failed")
#                     time.sleep(2)  # Wait 2 seconds before retry
#             except Exception as e:
#                 logger.error(f"Connection attempt {attempt + 1} failed with error: {e}")
#                 time.sleep(2)
        
#         logger.error("All connection attempts failed")
#         return False

# class RemoteDataService:
#     def __init__(self):
#         self.sdk = None
#         self.thread = None
#         self.running = False
#         self.connection_status = "disconnected"
#         self.last_error = None

#     def start_service(self, base_id=1, mode="auto"):
#         if self.running:
#             logger.warning("Service is already running")
#             return False

#         try:
#             self.sdk = DjangoEasyTestHandler()
#             self.connection_status = "connecting"
            
#             # Try to connect with retry logic
#             if self.sdk.connect_with_retry(base_id, mode):
#                 self.running = True
#                 self.connection_status = "connected"
#                 self.last_error = None
                
#                 # Start monitoring in a separate thread
#                 self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
#                 self.thread.start()
                
#                 logger.info("🔄 Remote data service started successfully")
#                 return True
#             else:
#                 self.connection_status = "failed"
#                 self.last_error = "Failed to connect after multiple attempts"
#                 return False
                
#         except Exception as e:
#             self.connection_status = "error"
#             self.last_error = str(e)
#             logger.error(f"Failed to start remote data service: {e}")
#             return False

#     def stop_service(self):
#         if not self.running:
#             return True

#         self.running = False
#         self.connection_status = "disconnected"
        
#         if self.sdk:
#             # Add cleanup code here if your EasyTest class supports it
#             try:
#                 # If your EasyTest has a disconnect method, call it here
#                 # self.sdk.disconnect()
#                 pass
#             except Exception as e:
#                 logger.error(f"Error during disconnect: {e}")
            
#         logger.info("🛑 Remote data service stopped")
#         return True

#     def _monitor_loop(self):
#         """Keep the service running and monitor connection"""
#         try:
#             while self.running:
#                 # Add health check here if your EasyTest supports it
#                 # You might want to ping the device periodically
#                 time.sleep(1)
#         except Exception as e:
#             logger.error(f"Error in monitor loop: {e}")
#             self.running = False
#             self.connection_status = "error"
#             self.last_error = str(e)

#     def get_status(self):
#         return {
#             'running': self.running,
#             'connection_status': self.connection_status,
#             'last_error': self.last_error,
#             'connected_devices': Device.objects.filter(status='connected').count(),
#             'total_events': KeypadEvent.objects.count(),
#             'active_vote_sessions': VoteSession.objects.filter(status='active').count()
#         }

#     def reconnect(self, base_id=1, mode="auto"):
#         """Force reconnection"""
#         if self.running:
#             self.stop_service()
#             time.sleep(1)
        
#         return self.start_service(base_id, mode)

# # Global service instance
# remote_service = RemoteDataService()



# remote_service.py
import threading
import time
import logging
from datetime import datetime, timezone as dt_timezone

from django.utils import timezone
from django.db import transaction

from .models import Device, KeypadEvent, VoteSession
from core.easy_test import EasyTest  # your SDK wrapper

logger = logging.getLogger(__name__)


class DjangoEasyTestHandler(EasyTest):
    """
    Adapter around EasyTest SDK to persist device/connect/key events to Django models.
    """

    def __init__(self):
        super().__init__()
        self.running = False
        self.connection_attempts = 0
        self.max_connection_attempts = 5

    def _on_connect(self, base_id, mode, info):
        """
        Called by the SDK on device connect.
        base_id: int/str
        mode, info: bytes (expected) or str
        """
        # decode safely
        try:
            mode_str = mode.decode() if isinstance(mode, (bytes, bytearray)) else (mode or "")
            info_str = info.decode() if isinstance(info, (bytes, bytearray)) else (info or "")
        except Exception:
            mode_str = str(mode)
            info_str = str(info)

        logger.info(f"📡 Device Connected: ID={base_id}, Mode={mode_str}, Info={info_str}")

        try:
            with transaction.atomic():
                device, created = Device.objects.get_or_create(
                    base_id=str(base_id),
                    defaults={
                        'mode': mode_str,
                        'info': info_str,
                        'status': 'connected'
                    }
                )

                if not created:
                    device.mode = mode_str
                    device.info = info_str
                    device.status = 'connected'
                    device.save(update_fields=['mode', 'info', 'status'])

                # Auto-start vote if info is exactly "1" (string)
                if info_str == "1":
                    logger.info(f"Auto-starting vote for device {base_id}")
                    try:
                        # Use the handler method; adjust args as per your SDK
                        self.vote_start(0, 10, "1,1,0,0,4,1")
                    except Exception as e:
                        logger.exception(f"Failed to call vote_start: {e}")

                    # Create VoteSession record
                    try:
                        VoteSession.objects.create(
                            device=device,
                            session_id=0,
                            duration=10,
                            config="1,1,0,0,4,1",
                            status='active'
                        )
                    except Exception as e:
                        logger.exception(f"Failed to create VoteSession DB record: {e}")

                logger.info(f"Device {base_id} {'created' if created else 'updated'} in database")

        except Exception as e:
            logger.exception(f"Error handling device connection: {e}")

    def _on_key(self, base_id, key_id, key_sn, mode, timestamp, info):
        """
        Called by SDK when a keypad event occurs.
        - key_sn, mode, info can be bytes; decode safely.
        - timestamp may be epoch seconds (int) or str bytes — convert to timezone-aware datetime.
        """
        # decode values safely
        try:
            key_sn_str = key_sn.decode() if isinstance(key_sn, (bytes, bytearray)) else (key_sn or "")
        except Exception:
            key_sn_str = str(key_sn)

        try:
            info_str = info.decode().strip() if isinstance(info, (bytes, bytearray)) else (str(info).strip() if info is not None else "")
        except Exception:
            info_str = str(info).strip()

        try:
            mode_str = mode.decode() if isinstance(mode, (bytes, bytearray)) else (mode or "")
        except Exception:
            mode_str = str(mode)

        # Normalize timestamp into a timezone-aware datetime
        event_time = None
        try:
            if isinstance(timestamp, (int, float)):
                event_time = datetime.fromtimestamp(float(timestamp), dt_timezone.utc)
            elif isinstance(timestamp, (bytes, bytearray)):
                # try decode then parse int
                ts_str = timestamp.decode()
                event_time = datetime.fromtimestamp(float(ts_str), dt_timezone.utc)
            elif isinstance(timestamp, str):
                # try parse as integer epoch seconds or ISO string fallback
                try:
                    event_time = datetime.fromtimestamp(float(timestamp), dt_timezone.utc)
                except Exception:
                    # fallback try to parse ISO format
                    event_time = datetime.fromisoformat(timestamp)
                    # ensure timezone-aware
                    if event_time.tzinfo is None:
                        event_time = event_time.replace(tzinfo=dt_timezone.utc)
            else:
                # fallback to now
                event_time = timezone.now()
        except Exception as e:
            logger.warning(f"Could not parse timestamp {timestamp!r}: {e}. Using timezone.now()")
            event_time = timezone.now()

        logger.info(
            f"🧭 Keypad Event: BaseID={base_id}, KeyID={key_id}, SN={key_sn_str}, Mode={mode_str}, "
            f"Info={repr(info_str)}, Time={event_time.isoformat()}"
        )

        try:
            with transaction.atomic():
                device = Device.objects.get(base_id=str(base_id))

                KeypadEvent.objects.create(
                    device=device,
                    key_id=key_id,
                    key_sn=key_sn_str,
                    mode=mode_str,
                    timestamp=event_time,
                    info=info_str,
                    processed=False
                )

                logger.info(f"Keypad event saved for device {base_id}")

        except Device.DoesNotExist:
            logger.error(f"Device with base_id {base_id} not found in database")
        except Exception as e:
            logger.exception(f"Error saving keypad event: {e}")

    def connect_with_retry(self, base_id, mode):
        """Try to connect with retry logic using self.connect(base_id, mode)."""
        for attempt in range(1, self.max_connection_attempts + 1):
            try:
                logger.info(f"Connection attempt {attempt}/{self.max_connection_attempts} to base_id={base_id} mode={mode}")
                # Assume EasyTest.connect returns True on success, False otherwise
                result = self.connect(base_id, mode)
                if result:
                    logger.info("Connection successful!")
                    return True
                else:
                    logger.warning(f"Connection attempt {attempt} returned False")
            except Exception as e:
                logger.exception(f"Connection attempt {attempt} failed with error: {e}")

            # wait before next attempt
            time.sleep(2)

        logger.error("All connection attempts failed")
        return False

    # Optional: implement disconnect hook if EasyTest supports it
    def safe_disconnect(self):
        try:
            if hasattr(self, "disconnect"):
                self.disconnect()
                logger.info("SDK disconnect called")
        except Exception as e:
            logger.exception(f"Error while disconnecting SDK: {e}")


class RemoteDataService:
    def __init__(self):
        self.sdk = None
        self.thread = None
        self.running = False
        self.connection_status = "disconnected"
        self.last_error = None

    def start_service(self, base_id=1, mode="auto"):
        if self.running:
            logger.warning("Service is already running")
            return False

        try:
            self.sdk = DjangoEasyTestHandler()
            self.connection_status = "connecting"

            # Try to connect with retry logic
            if self.sdk.connect_with_retry(base_id, mode):
                self.running = True
                self.connection_status = "connected"
                self.last_error = None

                # Start monitoring in a separate thread
                self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
                self.thread.start()

                logger.info("🔄 Remote data service started successfully")
                return True
            else:
                self.connection_status = "failed"
                self.last_error = "Failed to connect after multiple attempts"
                return False

        except Exception as e:
            self.connection_status = "error"
            self.last_error = str(e)
            logger.exception(f"Failed to start remote data service: {e}")
            return False

    def stop_service(self):
        if not self.running:
            logger.info("Service not running; nothing to stop")
            return True

        self.running = False
        self.connection_status = "disconnecting"

        try:
            if self.sdk:
                # call safe disconnect if SDK supports it
                try:
                    self.sdk.safe_disconnect()
                except Exception:
                    # fallback to direct method if safe_disconnect not present
                    if hasattr(self.sdk, "disconnect"):
                        try:
                            self.sdk.disconnect()
                        except Exception as e:
                            logger.exception(f"Error during SDK.disconnect(): {e}")
        finally:
            self.connection_status = "disconnected"
            logger.info("🛑 Remote data service stopped")

        return True

    def _monitor_loop(self):
        """Keep the service running and monitor connection"""
        try:
            while self.running:
                # Place health checks / pings here if SDK supports it
                time.sleep(1)
        except Exception as e:
            logger.exception(f"Error in monitor loop: {e}")
            self.running = False
            self.connection_status = "error"
            self.last_error = str(e)

    def get_status(self):
        try:
            return {
                'running': self.running,
                'connection_status': self.connection_status,
                'last_error': self.last_error,
                'connected_devices': Device.objects.filter(status='connected').count(),
                'total_events': KeypadEvent.objects.count(),
                'active_vote_sessions': VoteSession.objects.filter(status='active').count()
            }
        except Exception as e:
            logger.exception(f"Error retrieving status data: {e}")
            return {
                'running': self.running,
                'connection_status': self.connection_status,
                'last_error': self.last_error
            }

    def reconnect(self, base_id=1, mode="auto"):
        """Force reconnection"""
        if self.running:
            self.stop_service()
            time.sleep(1)

        return self.start_service(base_id, mode)


# Global service instance
remote_service = RemoteDataService()
