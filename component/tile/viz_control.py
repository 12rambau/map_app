from sepal_ui import mapping as sm
from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts import decorator as sd
from sepal_ui.scripts import utils as su

from component import scripts
from component.message import cm
from component.model import VizModel


class VizControl(sm.MenuControl):
    def __init__(self, aoi_model, m):

        # save the map as a member
        self.m = m

        # define the models
        self.model = VizModel()
        self.aoi_model = aoi_model

        # create widgets
        self.slider = sw.Slider(
            label=cm.default_process.slider, class_="mt-5", thumb_label=True, v_model=0
        )
        self.text = sw.TextField(label=cm.default_process.textfield, v_model=None)

        # link the widgets to the model
        self.model.bind(self.slider, "slider_value").bind(self.text, "text_value")

        # create the btn and the alert beforehand to make it compatible with loading_button
        self.btn = sw.Btn()
        self.alert = sw.Alert()

        # construct the Tile with the widget we have initialized
        tile = sw.Tile(
            id_="default_viz_tile",
            title=cm.default_process.title,
            inputs=[self.slider, self.text],
            btn=self.btn,
            alert=self.alert,
        )

        # create the menu
        super().__init__("fas fa-cogs", tile)

        # now that the Tile is created we can link it to a specific function
        self.btn.on_event("click", self._on_run)

    @sd.loading_button(debug=True)
    def _on_run(self, widget, data, event):

        # check inputs
        su.check_input(self.aoi_model.name, cm.default_process.no_aoi)
        su.check_input(self.model.slider_value, cm.default_process.no_slider)
        su.check_input(self.model.text_value, cm.default_process.no_textfield)

        # launch the process
        csv_path = scripts.default_csv(
            output=self.alert,
            pcnt=self.model.slider_value,
            name=self.model.text_value,
        )

        # create maps
        dataset = scripts.default_maps(self.aoi_model.feature_collection, self.m)

        # update model
        self.model.csv_path = csv_path
        self.model.dataset = dataset

        # conclude the computation with a message
        self.alert.add_live_msg(cm.default_process.end_computation, "success")

        return
