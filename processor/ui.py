import logging

from pydoover import ui


def construct_ui(processor):
    ui_elems = (
        # create_multiplot(include_ph3=include_ph3, include_mid=include_mid),
        ui.AlertStream("significantEvents", "Notify me of any problems"),
        # ui.StateCommand("selectedCrop", "Crop", 
        #     user_options=[ui.Option(o['name'], o['display_name']) for o in processor.get_crop_choices()],
        #     default="grain_type_not_specified"
        # ),
        ui.NumericVariable("Test Var", "Test Variable ",
            dec_precision=1,
            form=ui.Widget.radial,
            ranges=[
                ui.Range("Low", 0, 20, ui.Colour.green),
                ui.Range("Warm", 20, 30, ui.Colour.yellow),
                ui.Range("High", 30, 40, ui.Colour.red),
            ]
        ),
        ui.BooleanVariable("testBool", "Recevied Uplink", default=False,),
                        
        ui.ConnectionInfo(name="connectionInfo",
            connection_type=ui.ConnectionType.periodic,
            connection_period=processor.get_connection_period(),
            next_connection=processor.get_connection_period(),
            offline_after=(4 * processor.get_connection_period()),
            allowed_misses=4,
        )
    )

    return ui_elems

