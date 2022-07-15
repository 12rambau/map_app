from ipyleaflet import WidgetControl
from sepal_ui import mapping as sm
from sepal_ui import sepalwidgets as sw

from .aoi_control import AoiControl
from .export_control import ExportControl
from .viz_control import VizControl


class MapTile(sw.Tile):
    def __init__(self):

        # create a map
        self.m = sm.SepalMap(zoom=3)  # to be visible on 4k screens
        self.m.add_control(
            sm.FullScreenControl(
                self.m, fullscreen=True, fullapp=True, position="topright"
            )
        )

        # create the analysis controls
        self.aoi_control = AoiControl(self.m)
        self.viz_control = VizControl(self.aoi_control.model, self.m)
        self.export_control = ExportControl(
            self.viz_control.model, self.aoi_control.model
        )

        # add them on the map
        self.m.add_control(self.viz_control)
        self.m.add_control(self.aoi_control)
        self.m.add_control(self.export_control)

        # create the tile
        super().__init__("map_tile", "", [self.m])

    def set_code(self, link):
        "add the code link btn to the map"

        btn = sm.MapBtn("fas fa-code", href=link, target="_blank")
        control = WidgetControl(widget=btn, position="bottomleft")
        self.m.add_control(control)

        return

    def set_wiki(self, link):
        "add the wiki link btn to the map"

        btn = sm.MapBtn("fas fa-book-open", href=link, target="_blank")
        control = WidgetControl(widget=btn, position="bottomleft")
        self.m.add_control(control)

        return

    def set_issue(self, link):
        "add the code link btn to the map"

        btn = sm.MapBtn("fas fa-bug", href=link, target="_blank")
        control = WidgetControl(widget=btn, position="bottomleft")
        self.m.add_control(control)

        return
