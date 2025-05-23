import logging, json, time, math, random
from datetime import datetime, timezone, timedelta

from pydoover.cloud.processor import ProcessorBase

from ui import construct_ui

class target(ProcessorBase):

    # ui_state_channel: Channel
    # ui_cmds_channel: Channel

    # significant_event_channel: Channel
    # activity_log_channel: Channel

    # mqtt_uplink_channel: Channel
    # mqtt_downlink_channel: Channel


    def setup(self):

        # Get the required channels
        self.ui_state_channel = self.api.create_channel("ui_state", self.agent_id)
        self.ui_cmds_channel = self.api.create_channel("ui_cmds", self.agent_id)
        
        self.significant_event_channel = self.api.create_channel("significantEvent", self.agent_id)
        # self.activity_log_channel = self.api.create_channel("activity_log", self.agent_id)

        self.mqtt_uplink_channel_name = "mqtt_uplink_recv"
        self.mqtt_uplink_channel = self.api.create_channel(self.mqtt_uplink_channel_name, self.agent_id)
        self.mqtt_downlink_channel = self.api.create_channel("device_downlinks", self.agent_id)

        # Construct the UI
        self._ui_elements = construct_ui(self)
        
        self.ui_manager.set_children(self._ui_elements)
        self.ui_manager.pull()

    def process(self):
        message_type = self.package_config.get("message_type")

        if message_type == "DEPLOY":
            self.on_deploy()
        elif message_type == "DOWNLINK":
            self.on_downlink()
        elif message_type == "UPLINK":
            self.on_uplink()
        elif message_type == "GENERATE_DUMMY_DATA":
            self.on_generate_dummy_data()

    def on_deploy(self):
        ## Run any deployment code here

        # Construct the UI
        self.ui_manager.push()

        ## Publish a dummy message to ui_cmds to trigger a full refresh
        self.ui_cmds_channel.publish(
            {},
            save_log=False
        )

        ### This is not required anymore as uplink processor is now triggered by ui_cmds published above
        ## Initialise the mqtt_downlinks
        # self.on_downlink()

        ### This is not required anymore as uplink processor is now triggered by ui_cmds published above
        # # Publish a dummy message to uplink to trigger a new process of data
        # last_uplink_packet = self.mqtt_uplink_channel.fetch_aggregate()
        # if last_uplink_packet is not None:
        #     self.mqtt_uplink_channel.publish(last_uplink_packet)

    def on_downlink(self):
        print("Downlink received")
        # Run any downlink processing code here

    def on_uplink(self):

        save_log_required = True

        # Run any uplink processing code here
        if not (self.message and self.message.id) or not (self.message.channel_name == self.mqtt_uplink_channel_name):
            
            logging.info("No trigger message passed - fetching last message")
            self.message = self.mqtt_uplink_channel.last_message

            save_log_required = False ## We don't want to show the device updating if we are just fetching the last message

        raw_message = self.message.fetch_payload()
        if raw_message is None:
            logging.info("No payload found in message - skipping processing")
            return
        
        
        ## Update the UI Values
        self.ui_manager.update_variable("testBool", True)

        ## Update the UI
        self.ui_manager.push(
            record_log=True,#save_log_required,
            # timestamp=timestamp,
            even_if_empty=True,
            publish_fields=["currentValue"],
        )

    ## This gets called before ui manager is constructed
    def get_connection_period(self):
        try:
            sleep_time_hrs = self.ui_manager.get_interaction("sleepTime").current_value
        except:
            sleep_time_hrs = 6

        return sleep_time_hrs * 60 * 60
