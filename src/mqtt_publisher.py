"""Best-effort MQTT publisher for traffic count summaries."""
import json
import logging

logger = logging.getLogger(__name__)


class MqttPublisher:
    def __init__(
        self,
        enabled=False,
        host="localhost",
        port=1883,
        topic="traffic/counts",
        qos=0,
        keepalive=30,
    ):
        self.client = None
        self.topic = topic
        self.qos = int(qos)

        if not enabled:
            logger.info("MQTT disabled by configuration.")
            return

        try:
            import paho.mqtt.client as mqtt

            try:
                self.client = mqtt.Client(
                    mqtt.CallbackAPIVersion.VERSION2
                )
            except (AttributeError, TypeError):
                self.client = mqtt.Client()

            self.client.connect(host, int(port), int(keepalive))
            self.client.loop_start()
            logger.info("MQTT connected to %s:%s", host, port)
        except Exception as exc:
            logger.warning(
                "MQTT unavailable (%s); continuing without publishing.", exc
            )
            self.client = None

    def publish(self, payload):
        if self.client is None:
            return False
        try:
            info = self.client.publish(
                self.topic,
                json.dumps(payload),
                qos=self.qos,
                retain=False,
            )
            if info.rc != 0:
                logger.warning("MQTT publish returned status %s", info.rc)
                return False
            return True
        except Exception as exc:
            logger.warning("MQTT publish failed: %s", exc)
            return False

    def close(self):
        if self.client is not None:
            try:
                self.client.loop_stop()
                self.client.disconnect()
            except Exception as exc:
                logger.debug("MQTT shutdown warning: %s", exc)
            self.client = None
