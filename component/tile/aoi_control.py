import ee
from sepal_ui import aoi
from sepal_ui import color as sc
from sepal_ui import mapping as sm
from sepal_ui.scripts import decorator as sd

__all__ = ["AoiControl"]


class AoiView(aoi.AoiView):
    """
    extend the aoi_view component from sepal_ui mapping to add
    the extra coloring parameters used in this application. We are forced to copy/paste
    the _update_aoi function
    """

    @sd.loading_button(debug=True)
    def _update_aoi(self, widget, event, data):
        """
        extention of the original method that display information on the map.
        In the ee display we changed the display parameters
        """

        # update the model
        self.model.set_object()

        # update the map
        if self.map_:
            [self.map_.remove_layer(lr) for lr in self.map_.layers if lr.name == "aoi"]
            self.map_.zoom_bounds(self.model.total_bounds())

            if self.ee:

                empty = ee.Image().byte()
                outline = empty.paint(
                    featureCollection=self.model.feature_collection, color=1, width=2
                )

                self.map_.addLayer(outline, {"palette": sc.primary}, "aoi")
            else:
                self.map_.add_layer(self.model.get_ipygeojson())

            self.map_.hide_dc()

        # tell the rest of the apps that the aoi have been updated
        self.updated += 1

        return


class AoiControl(sm.MenuControl):
    def __init__(self, m):

        gee_dir = "projects/earthengine-legacy/assets/users/bornToBeAlive/sepal_ui_test"

        # set the aoi_model to share it with the other components
        self.aoi_view = AoiView(map_=m, folder=gee_dir)
        self.aoi_view.elevation = 0
        self.aoi_view.class_list.add("pa-2")

        # safe the model as a member
        self.model = self.aoi_view.model

        super().__init__("fas fa-map-marker-alt", self.aoi_view, m=m)
